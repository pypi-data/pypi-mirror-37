"""\
Utilities to connect to ssl servers validating them with their certificate hash.
"""

import ssl
import socket
import hashlib
import functools
import logging

logger = logging.getLogger(__name__)

class InvalidFingerprint(Exception): pass

def client_socket_builder(*args, **kwargs):
    """\
Receives the same parameters as the ssl_connect method. 
 
:returns: a parameterless function that attempts to open a new connection each time is invoked 
"""
    return functools.partial(ssl_connect, *args, **kwargs)

def ssl_connect(host, port, fingerprints, timeout=None):
    """\
Connect to a SSL server and validate that the server fingerprint is proper.
 
:param host: Host to connect to.
:param port: Port to connect to.
:param fingerprints: List of acceptable server fingerprints. Each one is expressed as a hex-string.
:returns: connected socked.
:raises InvalidFingerprint: if the server fingerprint is not whitelisted.
"""
    
    try:
        fingerprints = [f.replace(":","").lower() for f in fingerprints]
        rv = ssl.wrap_socket(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
        rv.settimeout(timeout)
        rv.connect((host, port))
        rv.do_handshake(True)
        
        fingerprint = hashlib.sha256(rv.getpeercert(True)).hexdigest()
        
        if not fingerprint in fingerprints:
            rv.close()
            raise InvalidFingerprint(fingerprint)
        
        return rv
    
    except IOError:
        logger.exception("Error conection to %s:%s" % (host, port))
        return None

def close(s):
    """\
Properly close an SSL socket
 
:param s: socket to be closed
"""
    try:
        s.shutdown(socket.SHUT_RDWR)
        s.close()
    except:
        # ignore errors.
        pass


class MockSocket(object):
    """Simulates a socket to be read and written"""
    def __init__(self, *args):
        self.parts_to_read = args
        self.written_parts = []
        
    def read(self):
        if not self.parts_to_read:
            return b""
        
        rv = self.parts_to_read[0]
        self.parts_to_read = self.parts_to_read[1:]
        
        if rv is None:
            raise ssl.SSLError("Simulating a socket that timed out")
        
        return rv
    
    def sendall(self, buf):
        self.written_parts.append(buf)
        
    def shutdown(self, ignored):
        pass
    
    def close(self):
        pass
    
    def settimeout(self, ignored):
        pass
    
