from .app import BaseApp
from .message import Message, Tag, MsgType, TagNotFound
from . import comm

import threading
from six.moves import queue
import logging
import functools
import datetime
from slowbreak import bursty_queue

LOG = logging.getLogger(__name__)
LOG_IN = LOG.getChild("in")
LOG_OUT = LOG.getChild("out")

def not_new_order_or_cancel(message):
    return not message[0][1] in (MsgType.OrderCancelRequest, MsgType.NewOrderSingle)

def thread_fun(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        LOG.info(threading.current_thread().name + " started")
        try:
            f(*args, **kwargs)
            LOG.info(threading.current_thread().name + " finished gracefully")
        except:
            LOG.exception(threading.current_thread().name + " terminated abnormally")
            
    return decorated

class OutMessageStore(object): 
    
    def __init__(self, we, you, extra_header_fields_fun=None, seq_num=1):
        self.we = we
        self.you = you
        self.lock = threading.Lock()
        self.messages = []
        self.first_seq_num = seq_num
        self.extra_header_fields_fun = extra_header_fields_fun
        
    @property
    def next_seq_num(self):
        return self.first_seq_num + len(self.messages)
    
    def decorate(self, message):
        rv = Message(
            message[0],
            ( 34, b"%d" % self.next_seq_num),
            ( 49, self.we ),
            ( 52, datetime.datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3].encode('ascii') ),
            ( 56, self.you )
        )
        if self.extra_header_fields_fun:
            rv += self.extra_header_fields_fun(message)
        return rv + message[1:]
        
    def decorate_and_register(self, message):
        with self.lock:
            decorated = self.decorate(message)
            self.messages.append(decorated)
            
            return decorated
        
    def get(self, seq_num):
        with self.lock:
            index = seq_num - self.first_seq_num
            if index < 0:
                raise IndexError("Invalid seq_num %s" % seq_num)
            return self.messages[index]
        
    def drop(self, seq_num):
        with self.lock:
            new_first = seq_num + 1
            delta = new_first - self.first_seq_num
            
            del self.messages[:delta]
            
            self.first_seq_num = new_first
            
        LOG.info("Dropping %s messages. New first %s" % (delta, new_first))
    
    def __len__(self):
        with self.lock:
            return len(self.messages)


class SessionApp(BaseApp):
    
    class InvalidMessage(Exception):
        pass
    
    class SignalStop(Exception):
        pass
    
    class WaitTimeout(BaseException):
        pass
    
    class MasterThread(threading.Thread):
        def __init__(self, app):
            super(SessionApp.MasterThread, self).__init__(name="SessionApp.master")
            self.app = app
            self.out_queue = bursty_queue.BurstyQueue(app.send_period)
            
        def store_and_send(self, message):
            LOG.warning("Skipping message %r. Attempted to send in master thread" % message)
            self.app._on_msg_not_rcvd(message)
            
        def send(self, message):
            self.out_queue.put(
                lambda thread: thread.store_and_send(message),
                low_priority = self.app.low_priority(message)
            )
            
        def send_and_disconnect(self, message):
            def send_and_disconnect_action(thread):
                thread.store_and_send(message)
                self.app.gtfo = True
                raise self.app.SignalStop()
            
            self.out_queue.put(
                send_and_disconnect_action,
                low_priority = False
            )
            
        def stop_request(self):
            def stop_request_action(thread):
                raise SessionApp.SignalStop()
            
            self.out_queue.put(stop_request_action, low_priority = False)
            
        def stop_this_thread(self, thread):
            def stop_this_thread_action(other_thread):
                if thread is other_thread:
                    raise self.app.SignalStop()
                
            self.out_queue.put(stop_this_thread_action, low_priority = False)
            
        def gap_fill(self, seq_no):
            
            def gap_fill_action(thread):
                
                # Find next seq_no
                new_seq_no = self.app.oms.next_seq_num
                
                # Drop confirmed messages
                self.app.oms.drop(seq_no - 1)
                
                # Report not received messages
                for m in self.app.oms.messages:
                    LOG.warning("Gap fill: Msg not received %r" % m)
                    self.app._on_msg_not_rcvd(m)
                
                # Drop not sent messages
                self.app.oms.drop(new_seq_no)
                
                # Send gap fill
                self.app.oms.first_seq_num = seq_no
                decorated = self.app.oms.decorate(Message(
                    (35,b'4'),
                    (36,b'%d' %new_seq_no),
                    (123, b'Y')
                ))
                LOG_OUT.info("Sending %r" % decorated)
                thread.socket.sendall(decorated.to_buf())
                
                # Set expected sequence number for future interaction
                self.app.oms.first_seq_num = new_seq_no
                
            self.out_queue.put(gap_fill_action, low_priority = False)
            
        @thread_fun
        def run(self):
            while True:
                socket = self.app.socket_klass()
                
                if socket:
                    out_thread = self.app.OutThread(app=self.app, socket=socket, queue=self.out_queue)
                    out_thread.start()
    
                    in_thread = self.app.InThread(app=self.app, socket=socket, out_thread=out_thread)
                    in_thread.start()
                    
                    in_thread.join()
                    out_thread.join()
                    
                else: 
                    LOG.warn("Could not connect to the server :(")
    
                LOG.info("Sleeping %s seconds before reconnecting" % self.app.reconnect_time)
                while True:
                
                    if self.app.gtfo:
                        return # Get the fuck out requested
                    
                    try:
                        self.out_queue.get(timeout=self.app.reconnect_time, ignore_throttling=True)(self) # No write thread, handle this things here
                    except self.app.SignalStop:
                        pass # 
                    except queue.Empty:
                        break # Now it is time to reconnect
                        
                    

                if self.app.gtfo:
                    LOG.info("gtfo set. Finishing main thread.")
                    return # Get the fuck out requested
                
                if not self.app.reconnect:
                    LOG.info("reconnect is false. Finishing main thread.")
                    return 
                        
    
    class InThread(threading.Thread):
        def __init__(self, app, socket, out_thread):
            super(SessionApp.InThread, self).__init__(name="SessionApp.in")
            self.app = app
            self.socket = socket
            self.out_thread = out_thread

        @thread_fun      
        def run(self):
            try:
                self.socket.settimeout(self.app.heartbeat_time * 1.2) # timeout if heartbit is missing by over 20% of the expected time
                messages = Message.from_socket(self.socket)
                if self.app.reset_seq_nums:
                    self.app.next_in_seq_num = 1
                logon = next(messages)
            
                if logon is None:
                    LOG.error("Timed out reading while logging in")
                    return
                
                LOG_IN.info("Received %r" % logon)
                if MsgType.Logon != logon.get_field(Tag.MsgType):
                    LOG.error("Received %r instead of logon" % logon)
                    return

                try:
                    self.app._on_msg_in(logon)
                except Exception as e:
                    LOG.warning("Ignoring exception %s while processing message %r" % (e, logon), exc_info=True)
                    
                timed_out = False
                for message in messages:
                    try:
                        LOG_IN.info("Received %r" % message)
                        if message is None:
                            LOG.warning("Timeout while waiting for message")
                            if not timed_out:
                                timed_out = True
                                self.app.send(
                                    Message((35,b"1"), (112, b"TEST"))
                                )
                                continue
                            
                            # Missing test request
                            LOG.error("Timeout while waiting for test request, disconnecting")
                            return
                            
                        timed_out = False
                        self.app._on_msg_in(message)
                        
                        if MsgType.Logout == message.get_field(Tag.MsgType):
                            LOG.info("Received logout. Stopping thread")
                            return
                    except Exception as e:
                        LOG.warning("Ignoring exception %s while processing message %r" % (e, message), exc_info=True)
                raise Exception("Connection closed without logout")
            finally:
                self.app.master_thread.stop_this_thread(self.out_thread)                
        
    
    class OutThread(threading.Thread):
        def __init__(self, app, socket, queue):
            super(SessionApp.OutThread, self).__init__(name="SessionApp.out")
            
            self.app = app
            self.queue = queue
            self.socket = socket
            self.store_and_send = self.store_and_send_skip
            
        def store_and_send_skip(self, message):
            LOG.warning("Skipping message %r. Attempted to send before login" % message)
            self.app._on_msg_not_rcvd(message)
            
        def store_and_send_normal(self, message):
            decorated = self.app.oms.decorate_and_register(message)
            LOG_OUT.info("Sending %r" % decorated)
            self.socket.sendall(decorated.to_buf())
            
        @thread_fun            
        def run(self):
            try:
                # Empty message queue
                while True:
                    try:
                        self.queue.get(timeout=0, ignore_throttling=True)(self)
                    except queue.Empty:
                        break
                    
                if self.app.reset_seq_nums or not self.app.oms:
                    self.app.oms = OutMessageStore(
                        we=self.app.we, 
                        you=self.app.you, 
                        extra_header_fields_fun=self.app.extra_header_fields_fun,
                        seq_num=1
                    )  
                    
                # Newer messages will be sent
                self.store_and_send = self.store_and_send_normal
                
                # logon first
                logon_msg = Message(
                    (35, b'A'),
                    (98, b'0'),
                    (108, b'%d' % self.app.heartbeat_time),
                    (553, self.app.username),
                    (554, self.app.password),
                    (1137, self.app.app_ver_id)
                )

                if self.app.reset_seq_nums:
                    logon_msg.append(141, b"Y")
                
                if self.app.test_mode == True:
                    logon_msg.append(464, b"Y")
                elif self.app.test_mode == False:
                    logon_msg.append(464, b"N")
                # No 464 (Test message indicator) if test mode is None
                    
                self.store_and_send( logon_msg )

                while True:
                    try:
                        self.queue.get(timeout=self.app.heartbeat_time)(self)
                    except queue.Empty:
                        self.store_and_send(Message((35, b'0'))) # send keepalive on timeout 
    
                    if self.app.confirm_request_msg_count <= len(self.app.oms) and not self.app.waiting_for_confirmation:
                        self.store_and_send( Message(
                            (35, b'1'),
                            (112, b'CONFIRM ' + str(self.app.oms.next_seq_num))
                        ) )
                        self.app.waiting_for_confirmation = True
            except SessionApp.SignalStop:
                pass # stop gracefully when signalled
            finally:
                comm.close(self.socket) # also stops in thread if required

    def __init__(self, 
        socket_klass, 
        username, 
        password, 
        we, 
        you, 
        heartbeat_time=10,
        confirm_request_msg_count=100, 
        reconnect=False,
        reconnect_time=60,
        reset_seq_nums=False,
        send_period=0.1,
        low_priority=not_new_order_or_cancel,
        test_mode=None, 
        app_ver_id=b'9', # ROFEX default
        extra_header_fields_fun=None, 
        *args, 
        **kwargs
    ):
        super(SessionApp, self).__init__(*args, **kwargs)

        self.username = username
        self.password = password

        self.we = we
        self.you = you
        self.heartbeat_time = heartbeat_time
        self.confirm_request_msg_count = confirm_request_msg_count
        self.reconnect = reconnect
        self.reconnect_time = reconnect_time
        self.reset_seq_nums = reset_seq_nums
        self.waiting_for_confirmation=False
        self.send_period = send_period
        self.low_priority = low_priority
        self.test_mode = test_mode
        self.app_ver_id = app_ver_id
        self.extra_header_fields_fun = extra_header_fields_fun
        
        self.socket_klass = socket_klass
        
        self.oms = None # will be set in the out thread
        self.next_in_seq_num = 1
        
        self.gtfo = False # get the fuck out
        
        self.master_thread = self.MasterThread(app=self)
        self.master_thread.start()
            
    def logout(self, msg=b"User generated logout", timeout=10):
        self.gtfo = True
        self.send(
            Message(
                (35, b'5'),
                (58, msg)
            )
        )
        
    def on_msg_in(self, message):
        
        seq_num = int(message.get_field(34))
        pos_dup = b'Y' == message.get_field(43, b'N')
        
        if seq_num < self.next_in_seq_num:
            if not pos_dup:
                LOG.error("Expecting seq_num %s but got %s. Disconnecting" % (self.next_in_seq_num, seq_num))
                self.disconnect()
            return # message already processed
            
        if seq_num > self.next_in_seq_num:
            # Resend request
            LOG.warning("Resend request starting at %s" % self.next_in_seq_num)
            self.send(
                Message(
                    (35,b'2'),
                    (7,b"%d" % self.next_in_seq_num),
                    (16,b"0")
                )
            )
            return
        
        # Everything is fine :D
        self.next_in_seq_num += 1
        
        _type = message.get_field(35)
        
        if MsgType.TestRequest == _type:
            req_id = message.get_field(112)
            self.send(
                Message(
                    (35, b'0'),
                    (112, req_id)
                )
            )
        elif MsgType.Heartbeat == _type:
            try:
                confirm = message.get_field(112)
                if confirm.startswith(b"CONFIRM "):
                    conf_seq_num = int(confirm[len(b"CONFIRM "):].encode('ascii'))
                    LOG.debug("Message %s confirmed" % conf_seq_num)
                    self.oms.drop(conf_seq_num)
                    self.waiting_for_confirmation = False
            except TagNotFound:
                pass
        elif MsgType.ResendRequest == _type:
            self.master_thread.gap_fill(int(message.get_field(7)))
        
        return message
        
    def send(self, message):
        if 35 != message[0][0]:
            raise self.InvalidMessage('First tag in message must be 35 for message %r' % message)
        
        self.master_thread.send(message)
        
    def disconnect(self):
        self.master_thread.stop_request()
        
    def force_stop(self):
        self.gtfo = True
        self.disconnect()
        
    def wait(self, timeout=None):
        self.master_thread.join(timeout)
        if self.master_thread.is_alive():
            raise self.WaitTimeout()


    