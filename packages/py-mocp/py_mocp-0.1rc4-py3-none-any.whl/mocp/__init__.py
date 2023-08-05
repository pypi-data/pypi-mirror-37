# -*- coding: utf-8 -*-

import os
import errno
import fcntl
import socket
import struct
import logging

from . import protocol
from . import exceptions

from time import sleep
from queue import Queue, Empty
from collections import defaultdict

__all__ = ['protocol', 'exceptions']

log = logging.getLogger('mocp')
log.addHandler(logging.NullHandler())


class MocSocket:
    """
    This class implements basic methods to communicate with MOC Player via unix socket.
    """  # NOQA
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
            raise exceptions.MocSocketConnectionError(
                "Can't connect to the server!")

    def get_int_noblock(self):
        """Get int from socket in non-blocking mode."""
        if not isinstance(self.socket, socket.socket):
            raise exceptions.MocSocketConnectionError(
                "Client is not connected")

        result = None
        flags = None
        try:
            flags = fcntl.fcntl(self.socket, fcntl.F_GETFL)
        except IOError as err:
            raise exceptions.MocSocketIOError(
                "Getting flags for socket failed: %s" % err)

        flags |= os.O_NONBLOCK

        try:
            fcntl.fcntl(self.socket, fcntl.F_SETFL, os.O_NONBLOCK)
        except IOError as err:
            raise exceptions.MocSocketIOError(
                "Setting O_NONBLOCK for the socket failed: %s" % err)

        try:
            data = self.socket.recv(struct.calcsize('i'))
            result = struct.unpack('i', data)[0]
        except socket.error as serr:
            if serr.errno not in (errno.EAGAIN, errno.EWOULDBLOCK):
                raise exceptions.MocSocketIOError(
                    "socket.recv failed when getting int: %s" % serr)

        flags &= ~os.O_NONBLOCK
        try:
            fcntl.fcntl(self.socket, fcntl.F_SETFL, flags)
        except IOError as err:
            raise exceptions.MocSocketIOError(
                "Restoring flags for socket failed: %s" % err)

        return result

    def get_int(self):
        """Get int from socket."""
        if not isinstance(self.socket, socket.socket):
            raise exceptions.MocSocketConnectionError(
                "Client is not connected")

        try:
            data = self.socket.recv(struct.calcsize('i'))
            return struct.unpack('i', data)[0]
        except socket.error:
            raise exceptions.MocSocketIOError(
                "Can't receive value from the server!")

    def get_str(self):
        """Get string from socket."""
        if not isinstance(self.socket, socket.socket):
            raise exceptions.MocSocketConnectionError(
                "Client is not connected")

        try:
            str_length = self.get_int()
            assert str_length <= self.MAX_SEND_STRING
            data = self.socket.recv(str_length, 0)
            return struct.unpack("%ds" % str_length, data)[0].decode()
        except AssertionError:
            raise exceptions.MocSocketIOError(
                "Bad string length.")
        except socket.error:
            raise exceptions.MocSocketIOError(
                "Can't receive string from the server!")

    def get_tags(self):
        """Get tags from socket."""
        if not isinstance(self.socket, socket.socket):
            raise exceptions.MocSocketConnectionError(
                "Client is not connected")

        try:
            title = self.get_str()
            artist = self.get_str()
            album = self.get_str()
            track = self.get_int()
            time = self.get_int()
            filled = self.get_int()
            return title, artist, album, track, time, filled
        except socket.error:
            raise exceptions.MocSocketIOError(
                "Can't receive tags from the server!")

    def get_time(self):
        """Get time from socket."""
        if not isinstance(self.socket, socket.socket):
            raise exceptions.MocSocketConnectionError(
                "Client is not connected")

        try:
            data = self.socket.recv(struct.calcsize('l'), 0)
            return struct.unpack('L', data)[0]
        except socket.error:
            raise exceptions.MocSocketIOError(
                "Can't receive value from the server!")

    def send_int(self, value):
        """Send int to socket."""
        if not isinstance(self.socket, socket.socket):
            raise exceptions.MocSocketConnectionError(
                "Client is not connected")

        try:
            self.socket.send(struct.pack("I", value))
        except socket.error:
            raise exceptions.MocSocketIOError(
                "Can't send() value to the server!")

    def send_str(self, value):
        """Send string to socket."""
        if not isinstance(self.socket, socket.socket):
            raise exceptions.MocSocketConnectionError(
                "Client is not connected")

        try:
            s = value.encode()
            self.socket.send(struct.pack("I%ds" % (len(s),), len(s), s))
        except socket.error:
            raise exceptions.MocSocketIOError(
                "Can't send() string to the server!")

    def disconnect(self):
        """Disconnect from mocp server."""
        if self.socket:
            self.socket.shutdown(1)
            self.socket.close()
            self.socket = None


class FileTags(object):
    """
    This class implements struct file_tags from moc-2.6.0~svn-r2935/playlist.h
    """

    TAGS_COMMENTS = 0x01  # artist, title, etc.
    TAGS_TIME = 0x02  # time of the file.

    def __init__(self, title, artist, album, track, time, filled):
        """
        Constructor.

        @param title: Song title
        @type title: string

        @param artist: Artist name
        @type artist: string

        @param album: Album name
        @type album: string

        @param track: Track number
        @type album: int

        @param time: Track total time
        @type album: int

        @param filled: Which tags are filled: TAGS_COMMENTS, TAGS_TIME.
        @type album: int
        """
        self.title = title
        self.artist = artist
        self.album = album
        self.track = track
        self.time = time
        self.filled = filled

    def __eq__(self, other):
        assert isinstance(other, self.__class__), "Can't compare object with %r" % other  # NOQA
        for key in self.__dict__:
            if self.__dict__[key] != other.__dict__[key]:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        if self.artist and self.title:
            return True
        return False

    def __str__(self):
        album = ''
        if len(self.album):
            album = '(%s)' % self.album
        artist = ''
        if len(self.artist):
            artist = '%s -' % self.artist
        return ' '.join([artist, self.title, album]).strip()

    def __repr__(self):
        return '<Track: %s>' % self


class MocClient(object):
    """
    This class is basic implementation of MOC Player client.
    """
    def __init__(self, socket_file=os.path.expanduser("~/.moc/socket2")):
        """
        Constructor.

        @param socket_file: Path to unix socket file.
        @type socket_file: string
        """
        self.socket = MocSocket(socket_file)

        self.events = Queue()
        self.events.put((protocol.event.EV_OPTIONS, None))
        self.events.put((protocol.event.EV_STATE, ('', FileTags('', '', '', -1, -1, 0))))  # NOQA

        self.server_state = protocol.state.STATE_STOP
        self.current_time = 0
        self.current_file = ''
        self.bitrate = -1
        self.rate = -1
        self.channels = 2
        self.status_msg = ''
        self.server_options = {}
        self.file_tags = FileTags('', '', '', -1, -1, 0)
        self.mixer_name = ''
        self.avg_bitrate = -1

    def __wait_for_data(self):
        """
        This method implements wait_for_data function
        from moc-2.6.0~svn-r2935/interface.c file
        """
        event = None
        while event != protocol.event.EV_DATA:
            event = self.socket.get_int()
            if event == protocol.event.EV_EXIT:
                log.debug("The server exited!")
            if event != protocol.event.EV_DATA:
                self.events.put((event, self.__get_event_data(event)))

    def __get_data_int(self):
        """
        This method implements get_data_int function
        from moc-2.6.0~svn-r2935/interface.c file
        """
        self.__wait_for_data()
        return self.socket.get_int()

    def __get_data_str(self):
        """
        This method implements get_data_str function
        from moc-2.6.0~svn-r2935/interface.c file
        """
        self.__wait_for_data()
        return self.socket.get_str()

    def __get_data_bool(self):
        """
        This method implements get_data_bool function
        from moc-2.6.0~svn-r2935/interface.c file
        """
        self.__wait_for_data()
        if self.socket.get_int() == 1:
            return True
        return False

    def __get_data_tags(self):
        """
        This method implements get_data_tags function
        from moc-2.6.0~svn-r2935/interface.c file
        """
        self.__wait_for_data()
        return self.socket.get_tags()

    def __recv_item_data(self):
        """
        This method implements recv_item_from_srv function
        from moc-2.6.0~svn-r2935/interface.c file
        """
        class objectview(object):
            def __init__(self, d):
                self.__dict__.update(d)

        data = {}
        data['file'] = self.socket.get_str()
        if len(data['file']):
            data['title_tags'] = self.socket.get_str()

        data['tags'] = self.socket.get_tags()

        return objectview(data)

    def __recv_move_ev_data(self):
        """
        This method implements recv_tags_data_from_srv function
        from moc-2.6.0~svn-r2935/interface.c file
        """
        class objectview(object):
            def __init__(self, d):
                self.__dict__.update(d)

        data = {}
        data['item_from'] = self.socket.get_str()
        data['item_to'] = self.socket.get_str()

        return objectview(data)

    def __get_event_data(self, event):
        """
        This method implements get_event_data function
        from moc-2.6.0~svn-r2935/interface.c file
        """
        if event in (protocol.event.EV_PLIST_ADD, protocol.event.EV_QUEUE_ADD):
            return self.__recv_item_data()
        elif event in (protocol.event.EV_PLIST_DEL,
                       protocol.event.EV_QUEUE_DEL,
                       protocol.event.EV_STATUS_MSG,
                       protocol.event.EV_SRV_ERROR):
            return self.socket.get_str()
        elif event == protocol.event.EV_FILE_TAGS:
            return self.socket.get_str(), FileTags(*self.socket.get_tags())
        elif event in (protocol.event.EV_PLIST_MOVE,
                       protocol.event.EV_QUEUE_MOVE):
            return self.__recv_move_ev_data()
        return None

    def __handle_server_event(self, event, data=None):
        """
        This method implements server_event function
        from moc-2.6.0~svn-r2935/interface.c file
        """
        if event == protocol.event.EV_BUSY:
            log.debug("The server is busy; too many other clients are connected!")  # NOQA
            raise exceptions.MocServerBusy
        elif event == protocol.event.EV_CTIME:
            self.socket.send_int(protocol.command.CMD_GET_CTIME)
            self.current_time = self.__get_data_int()
        elif event == protocol.event.EV_STATE:
            # Update state
            self.socket.send_int(protocol.command.CMD_GET_STATE)
            self.server_state = self.__get_data_int()
            # Update current file
            self.socket.send_int(protocol.command.CMD_GET_SNAME)
            file_path = self.__get_data_str()
            if (not file_path or self.server_state == protocol.state.STATE_STOP):  # NOQA
                # Nothing is played/paused.
                self.current_file = ''
            elif (file_path and (not self.current_file or file_path != self.current_file)):  # NOQA
                # played file has changed
                self.current_file = file_path
                if self.current_file.startswith(('http://', 'ftp://')):
                    self.socket.send_int(protocol.command.CMD_GET_TAGS)
                    self.file_tags = FileTags(*self.__get_data_tags())
                else:
                    self.socket.send_int(protocol.command.CMD_GET_FILE_TAGS)
                    self.socket.send_str(file_path)
                    self.socket.send_int(FileTags.TAGS_COMMENTS | FileTags.TAGS_TIME)  # NOQA
            # Update channels
            self.events.put((protocol.event.EV_CHANNELS, None))
            # Update bitrate
            self.events.put((protocol.event.EV_BITRATE, None))
            # Update avr bitrate
            self.events.put((protocol.event.EV_AVG_BITRATE, None))
            # Update rate
            self.events.put((protocol.event.EV_RATE, None))
            # Update current
            self.events.put((protocol.event.EV_CTIME, None))
        elif event == protocol.event.EV_EXIT:
            log.debug("The server exited!")
            raise exceptions.MocServerExited
        elif event == protocol.event.EV_BITRATE:
            self.socket.send_int(protocol.command.CMD_GET_BITRATE)
            self.bitrate = self.__get_data_int()
        elif event == protocol.event.EV_RATE:
            self.socket.send_int(protocol.command.CMD_GET_RATE)
            self.rate = self.__get_data_int()
        elif event == protocol.event.EV_CHANNELS:
            self.socket.send_int(protocol.command.CMD_GET_CHANNELS)
            self.channels = 2
            if self.__get_data_int() != 2:
                self.channels = 1
        elif event == protocol.event.EV_SRV_ERROR:
            # FIXME: Handle error messages from server
            log.debug('Recieved error message from server: ' % data)
        elif event == protocol.event.EV_OPTIONS:
            for opt in ["Shuffle", "Repeat", "AutoNext"]:
                self.socket.send_int(protocol.command.CMD_GET_OPTION)
                self.socket.send_str(opt)
                self.server_options[opt] = self.__get_data_bool()
        elif event == protocol.event.EV_SEND_PLIST:
            # FIXME: Handle EV_SEND_PLIST event
            pass
        elif event == protocol.event.EV_PLIST_ADD:
            # FIXME: Handle EV_PLIST_ADD event
            pass
        elif event == protocol.event.EV_PLIST_CLEAR:
            # FIXME: Handle EV_PLIST_CLEAR event
            pass
        elif event == protocol.event.EV_PLIST_DEL:
            # FIXME: Handle EV_PLIST_DEL event
            pass
        elif event == protocol.event.EV_PLIST_MOVE:
            # FIXME: Handle EV_PLIST_MOVE event
            pass
        elif event == protocol.event.EV_TAGS:
            # Use new tags for current file title (for Internet streams).
            if self.current_file.startswith(('http://', 'ftp://')):
                self.socket.send_int(protocol.command.CMD_GET_TAGS)
                self.file_tags = FileTags(*self.__get_data_tags())
        elif event == protocol.event.EV_STATUS_MSG:
            self.status_msg = data
        elif event == protocol.event.EV_MIXER_CHANGE:
            self.socket.send_int(protocol.command.CMD_GET_MIXER_CHANNEL_NAME)
            self.mixer_name = self.__get_data_str()
        elif event == protocol.event.EV_FILE_TAGS:
            self.current_file, self.file_tags = data
        elif event == protocol.event.EV_AVG_BITRATE:
            self.socket.send_int(protocol.command.CMD_GET_AVG_BITRATE)
            self.avg_bitrate = self.__get_data_int()
        elif event == protocol.event.EV_QUEUE_ADD:
            # FIXME: Handle EV_QUEUE_ADD event
            pass
        elif event == protocol.event.EV_QUEUE_DEL:
            # FIXME: Handle EV_QUEUE_DEL event
            pass
        elif event == protocol.event.EV_QUEUE_CLEAR:
            # FIXME: Handle EV_QUEUE_CLEAR event
            pass
        elif event == protocol.event.EV_QUEUE_MOVE:
            # FIXME: Handle EV_QUEUE_MOVE event
            pass
        elif event == protocol.event.EV_AUDIO_START:
            self.server_state = protocol.state.STATE_PLAY
        elif event == protocol.event.EV_AUDIO_STOP:
            self.server_state = protocol.state.STATE_STOP
            self.current_time = 0
            self.current_file = ''
            self.bitrate = -1
            self.rate = -1
            self.channels = 2
            self.status_msg = ''
            self.server_options = {}
            self.file_tags = FileTags('', '', '', 0, 0, 0)
            self.mixer_name = ''
            self.avg_bitrate = -1
        else:
            log.debug("Unknown event: 0x%02x!" % event)

    def update(self):
        """Initiate the update process."""
        log.debug("Dequeuing events...")
        while True:
            try:
                event, data = self.events.get_nowait()
                log.debug("Received event: 0x%02x" % event)
                self.__handle_server_event(event, data)
            except Empty:
                break
        event = self.socket.get_int_noblock()
        if event:
            data = self.__get_event_data(event)
            log.debug("Received event: 0x%02x" % event)
            self.__handle_server_event(event, data)

    def run(self):
        """Runs the update method continuously."""
        self.socket.connect()
        self.events = Queue()
        while True:
            self.update()
            sleep(0.1)

    def __del__(self):
        """
        Destructor.

        Force close socket even if an error occurred on clients/servers side.
        """
        self.events = Queue()
        self.socket.disconnect()


class MocEventLoop(MocClient):
    """An event loop."""
    ALLOWED_SIGNALS = [
        'on_server_state', 'on_file_changed', 'on_status_changed',
        'on_title_changed', 'on_current_time_changed', 'on_bitrate_changed',
        'on_avr_bitrate_changed', 'on_rate_changed', 'on_channels_changed'
    ]

    def __init__(self, socket_file=os.path.expanduser("~/.moc/socket2")):
        """
        Constructor.

        @param socket_file: Path to unix socket file.
        @type socket_file: string
        """
        super(MocEventLoop, self).__init__(socket_file)
        self._event_callbacks = defaultdict(list)
        self._server_state_old = self.server_state
        self._current_time_old = self.current_time
        self._current_file_old = self.current_file
        self._bitrate_old = self.bitrate
        self._rate_old = self.rate
        self._channels_old = self.channels
        self._status_msg_old = self.status_msg
        self._file_tags_old = self.file_tags
        self._avg_bitrate_old = self.avg_bitrate

    def register(self, event, callback):
        """
        Method used to register a callback for `event`

        @param event: Event name.
        @type event: string

        @param callback: Some function.
        @type callback: callable
        """
        if event not in self.ALLOWED_SIGNALS:
            raise exceptions.MocError('Unsupported event type -> %s' % event)

        if not hasattr(callback, '__call__'):
            raise exceptions.MocError('`callback` param must be callable')

        self._event_callbacks[event].append(callback)

    def run(self):
        """
        Runs the update method continuously and calls registered callbacks.
        """
        while True:
            try:
                self.socket.connect()
                self.events = Queue()
                while True:
                    self.update()
                    if self._server_state_old != self.server_state:
                        self._server_state_old = self.server_state
                        for callback in self._event_callbacks['on_server_state']:  # NOQA
                            callback(self.server_state)

                    if self._status_msg_old != self.status_msg:
                        self._status_msg_old = self.status_msg
                        for callback in self._event_callbacks['on_status_changed']:  # NOQA
                            callback(self.status_msg)

                    if not self.current_file:
                        continue

                    if self._current_file_old != self.current_file:
                        self._current_file_old = self.current_file
                        for callback in self._event_callbacks['on_file_changed']:  # NOQA
                            callback(self.current_file)

                    if self._file_tags_old != self.file_tags:
                        self._file_tags_old = self.file_tags
                        if self.current_file.startswith(('http://', 'ftp://')) and not str(self.file_tags):  # NOQA
                            # Stream without title? Looks like a bug.
                            pass
                        else:
                            for callback in self._event_callbacks['on_title_changed']:  # NOQA
                                callback(self.file_tags)

                    if self._current_time_old != self.current_time:
                        self._current_time_old = self.current_time
                        for callback in self._event_callbacks['on_current_time_changed']:  # NOQA
                            callback(self.current_time)

                    if self._bitrate_old != self.bitrate:
                        self._bitrate_old = self.bitrate
                        for callback in self._event_callbacks['on_bitrate_changed']:  # NOQA
                            callback(self.bitrate)

                    if self._avg_bitrate_old != self.avg_bitrate:
                        self._avg_bitrate_old = self.avg_bitrate
                        for callback in self._event_callbacks['on_avr_bitrate_changed']:  # NOQA
                            callback(self.avg_bitrate)

                    if self._rate_old != self.rate:
                        self._rate_old = self.rate
                        for callback in self._event_callbacks['on_rate_changed']:  # NOQA
                            callback(self.rate)

                    if self._channels_old != self.channels:
                        self._channels_old = self.channels
                        for callback in self._event_callbacks['on_channels_changed']:  # NOQA
                            callback(self.channels)

                    sleep(0.1)
            except (exceptions.MocServerExited,
                    exceptions.MocSocketConnectionError,
                    exceptions.MocSocketIOError):
                self.socket.disconnect()
                sleep(1)
