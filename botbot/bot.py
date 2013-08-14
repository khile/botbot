"""A simple socket interface."""
import socket

from multiprocessing import Process

from botbot.debug import debug


class Bot(object):
    """Socket bot"""

    def __init__(self, host, port, debug=False):
        """Initialize the bot with host and port. Debig is an optional
        flag that enables all reads and write to be displayed to the
        terminal.

        """
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect((host, port))
        self.debug = debug

    def close(self):
        """Close the socket"""
        self._s.close()

    def read(self, size=4096):
        """Read maximum size bytes from socket"""
        msg = str(self._s.recv(size), 'utf-8', errors='replace')
        if self.debug:
            Process(target=debug, args=(msg,)).start()
        return msg

    def write(self, msg):
        """Write all of message to socket"""
        self._s.sendall(bytes(msg, 'utf-8'))
        if self.debug:
            Process(target=debug, args=('>>> {}'.format(msg),)).start()
