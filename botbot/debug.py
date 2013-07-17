"""A way to handle debuging output"""
import os
import time

from multiprocessing import Process

from conf import LOG_FILE


def log(msg):
    """Log the msg to the log file"""
    msg = msg.encode('ascii', errors='replace')
    msg = str(msg, 'ascii', errors='replace')
    f = open(LOG_FILE, 'a')
    f.write(msg+'\n')
    f.close()

def display(msg):
    """Print the message to the terminal"""
    msg = msg.encode('ascii', errors='replace')
    msg = str(msg, 'ascii', errors='replace')
    print(msg)

def debug(msg, log_only=False, prefix=True):
    """Log and display the msg unless log_only is not the default value"""
    if prefix:
        now = time.strftime('%m.%d.%Y::%H:%M:%S>', time.localtime())
        msg = now + ' | ' + msg
    Process(target=log, args=(msg,)).start()
    if not log_only:
        Process(target=display, args=(msg,)).start()
