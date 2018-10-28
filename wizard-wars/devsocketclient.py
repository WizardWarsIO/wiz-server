import threading
from socketIO_client import SocketIO as socketIOclient
from socketIO_client import LoggingNamespace
sio = socketIOclient('localhost', 8100, LoggingNamespace)

def doLoop():
    sio.emit('masterloop')

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

set_interval(doLoop, 1)

