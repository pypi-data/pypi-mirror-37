import os
import errno
import fcntl
import socket
import struct

from .exceptions import (
    MocSocketConnectionError,
    MocSocketIOError
)


class MocSocketClient:
    """
    This class implements basic methods
    to communicate with mocp player via unix socket.
    """
    MAX_SEND_STRING = 4096

    def __init__(self, socket_file=os.path.expanduser("~/.moc/socket2")):
        """
        Constructor.

        @param socket_file: Path to unix socket file.
        @type socket_file: string
        """
        self.socket_file = socket_file
        self.socket = None

    def connect(self):
        """Connect to mocp server. Raise MocSocketConnectionError if can't."""
        self.disconnect()
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            self.socket.connect(self.socket_file)
        except Exception:
            raise MocSocketConnectionError("Can't connect to the server!")

    def get_int_noblock(self):
        """Get int from socket in non-blocking mode."""
        if not isinstance(self.socket, socket.socket):
            raise MocSocketConnectionError("Client is not connected")

        result = None
        flags = None
        try:
            flags = fcntl.fcntl(self.socket, fcntl.F_GETFL)
        except IOError as err:
            raise MocSocketIOError(
                "Getting flags for socket failed: %s" % err)

        flags |= os.O_NONBLOCK

        try:
            fcntl.fcntl(self.socket, fcntl.F_SETFL, os.O_NONBLOCK)
        except IOError as err:
            raise MocSocketIOError(
                "Setting O_NONBLOCK for the socket failed: %s" % err)

        try:
            data = self.socket.recv(struct.calcsize('i'))
            result = struct.unpack('i', data)[0]
        except socket.error as serr:
            if serr.errno not in (errno.EAGAIN, errno.EWOULDBLOCK):
                raise MocSocketIOError(
                    "socket.recv failed when getting int: %s" % serr)

        flags &= ~os.O_NONBLOCK
        try:
            fcntl.fcntl(self.socket, fcntl.F_SETFL, flags)
        except IOError as err:
            raise MocSocketIOError(
                "Restoring flags for socket failed: %s" % err)

        return result

    def get_int(self):
        """Get int from socket."""
        if not isinstance(self.socket, socket.socket):
            raise MocSocketConnectionError("Client is not connected")

        try:
            data = self.socket.recv(struct.calcsize('i'))
            return struct.unpack('i', data)[0]
        except socket.error:
            raise MocSocketIOError("Can't receive value from the server!")

    def get_str(self):
        """Get string from socket."""
        if not isinstance(self.socket, socket.socket):
            raise MocSocketConnectionError("Client is not connected")

        try:
            str_length = self.get_int()
            assert str_length <= self.MAX_SEND_STRING
            data = self.socket.recv(str_length, 0)
            return struct.unpack("%ds" % str_length, data)[0].decode()
        except AssertionError:
            raise MocSocketIOError("Bad string length.")
        except socket.error:
            raise MocSocketIOError("Can't receive string from the server!")

    def get_tags(self):
        """Get tags from socket."""
        if not isinstance(self.socket, socket.socket):
            raise MocSocketConnectionError("Client is not connected")

        try:
            title = self.get_str()
            artist = self.get_str()
            album = self.get_str()
            track = self.get_int()
            time = self.get_int()
            filled = self.get_int()
            return title, artist, album, track, time, filled
        except socket.error:
            raise MocSocketIOError("Can't receive tags from the server!")

    def get_time(self):
        """Get time from socket."""
        if not isinstance(self.socket, socket.socket):
            raise MocSocketConnectionError("Client is not connected")

        try:
            data = self.socket.recv(struct.calcsize('l'), 0)
            return struct.unpack('L', data)[0]
        except socket.error:
            raise MocSocketIOError("Can't receive value from the server!")

    def send_int(self, value):
        """Send int to socket."""
        if not isinstance(self.socket, socket.socket):
            raise MocSocketConnectionError("Client is not connected")

        try:
            self.socket.send(struct.pack("I", value))
        except socket.error:
            raise MocSocketIOError("Can't send() value to the server!")

    def send_str(self, value):
        """Send string to socket."""
        if not isinstance(self.socket, socket.socket):
            raise MocSocketConnectionError("Client is not connected")

        try:
            s = value.encode()
            self.socket.send(struct.pack("I%ds" % (len(s),), len(s), s))
        except socket.error:
            raise MocSocketIOError("Can't send() string to the server!")

    def disconnect(self):
        """Disconnect from mocp server."""
        if self.socket:
            self.socket.shutdown(1)
            self.socket.close()
            self.socket = None
