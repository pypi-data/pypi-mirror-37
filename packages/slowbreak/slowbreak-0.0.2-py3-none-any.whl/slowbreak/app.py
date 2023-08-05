"""
Base classes to do slowbreak applications
"""

class BaseApp(object):
    "Base class to be used to make chainable applications"
    
    def __init__(self, upper_klass=None, lower_app=None, send = None):
        self.upper_app = upper_klass(lower_app=self) if upper_klass else None
        self.lower_app = lower_app
        
    def _on_msg_in(self, message):
        message = self.on_msg_in(message)
        if message and self.upper_app:
            message = self.upper_app._on_msg_in(message)
            
        return message
    
    def on_msg_in(self, message):
        """\
Override to define what to do when a message is received from the other party. 

:param message: Received message 
:returns: message to be passed to the upper app. If None processing is stopped.
"""
        return message
    
    def _on_msg_not_rcvd(self, message):
        message = self.on_msg_not_rcvd(message)
        if message and self.upper_app:
            message = self.upper_app._on_msg_not_rcvd(message)
            
        return message
    
    def on_msg_not_rcvd(self, message):
        """\
Override to define what to do when a message was not sent to the other party. 

:param message: Message not received 
:returns: message to be passed to the upper app. If None processing is stopped.
"""
        return message

    
    def send(self, message):
        """\
Send message to the other party.

:param message: Message to be sent
"""
        message = self.on_send_request(message)
        if message:
            return self.lower_app.send(message)
    
    def on_send_request(self, message):
        """\
Override to define what to do with a message to be sent to the other party. 
This method is called when someone calls send on any application upper in the stack (including this one).
Can be used to stop a message to be sent to the other party. 

:param message: Message to be sent. 
:returns: message to be passed to the upper app. If None processing is stopped.
"""
        return message
    
def stack(*args):
    """\
Build stack of apps. Each parameter is for a layer in the stack. Bottom first.

:param *args: List of pairs (class, kwargs) for each app in the stack.
:returns: stack of applications.  

Sample usage:

    stack = app.stack(
        (
            session.SessionApp, 
            dict( 
                socket_klass = sb, 
                username = user,  
                password= password, 
                we = user, 
                you="NYSE",
                reset_seq_nums=True
            )
        ),
        (
            MyStrategyApp,
            dict(
                param1 = value1,
                param2 = value2
            )
        )
    )
"""
    
    if not args:
        raise Exception("Cannot make empty stack")
    
    if 1 == len(args):
        raise Exception("Cannot make stack of a single layer. Just run the app constructor!")
    
    # Generate upper constructor
    klass, kwargs = args[-1]
    upper_klass = (lambda klass, kwargs: lambda lower_app: klass(lower_app=lower_app, **kwargs))(klass, kwargs)
    
    def build_constructor(klass, kwargs, upper_klass):
        return lambda lower_app: klass(lower_app=lower_app, upper_klass=upper_klass, **kwargs)

    # Chain middle    
    for klass, kwargs in reversed(args[1:-1]): 
        upper_klass = build_constructor(klass, kwargs, upper_klass)
    
    # Generate base and return
    klass, kwargs = args[0]
    return klass(upper_klass=upper_klass, **kwargs)

def on(type_):
    """\
Decorator to be used with a ByMessageTypeApp to handle messages received of a certain type.
It looks at the field 35 of the message and compares with the type_.

Sample usage:
    @on(MsgType.ExecutionReport)
    def on_execution_report(self, message):
        # do something with the execution report
        return message # pass the message to the upper app if exists.

:param type_: type of the message to be handled. Can be a slowbreak.constants.MsgType constant.
:returns: decorator to be used with a ByMessageTypeApp method.
"""
    def decorator(f):
        f.on_type = type_
        return f
    
    return decorator

class ByMessageTypeApp(BaseApp):
    """\
Utility class to handle each type of message received separately.

Use the on(type_) decorator to mark a method for each type handled.
"""
    
    def __init__(self, *args, **kwargs):
        
        self.handlers = {}
        
        for n in dir(self):
            a = getattr(self, n)
            t = getattr(a, "on_type", None)
            if t:
                self.handlers[t] = a
        
        super(ByMessageTypeApp, self).__init__(*args, **kwargs)
    
    def on_msg_in(self, message):
        t = message.get_field(35)
        return self.handlers.get(
            t, self.on_unhandled
        )(message)
    
    def on_unhandled(self, message):
        """\
Method called when the type of the message received was not registered with the on(type_) decorator

:params message: Unhandled message
:returns: message to be passed to the upper app. If None processing is stopped.
"""
        return message
