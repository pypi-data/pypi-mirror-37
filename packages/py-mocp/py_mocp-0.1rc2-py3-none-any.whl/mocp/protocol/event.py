# Definition of events sent by server to the client.
EV_STATE = 0x01  # server has changed the state
EV_CTIME = 0x02  # current time of the song has changed
EV_SRV_ERROR = 0x04  # an error occurred
EV_BUSY = 0x05  # another client is connected to the server
EV_DATA = 0x06  # data in response to a request will arrive
EV_BITRATE = 0x07  # the bitrate has changed
EV_RATE = 0x08  # the rate has changed
EV_CHANNELS = 0x09  # the number of channels has changed
EV_EXIT = 0x0a  # the server is about to exit
EV_PONG = 0x0b  # response for CMD_PING
EV_OPTIONS = 0x0c  # the options has changed
EV_SEND_PLIST = 0x0d  # request for sending the playlist
EV_TAGS = 0x0e  # tags for the current file have changed
EV_STATUS_MSG = 0x0f  # followed by a status message
EV_MIXER_CHANGE = 0x10  # the mixer channel was changed
EV_FILE_TAGS = 0x11  # tags in a response for tags request
EV_AVG_BITRATE = 0x12  # average bitrate has changed (new song)
EV_AUDIO_START = 0x13  # playing of audio has started
EV_AUDIO_STOP = 0x14  # playing of audio has stopped

# Events caused by a client that wants to modify the playlist
EV_PLIST_ADD = 0x50  # add an item, followed by the file name
EV_PLIST_DEL = 0x51  # delete an item, followed by the file name
EV_PLIST_MOVE = 0x52  # move an item, followed by 2 file names
EV_PLIST_CLEAR = 0x53  # clear the playlist

# These events, though similar to the four previous are caused by server
# * which takes care of clients' queue synchronization.
EV_QUEUE_ADD = 0x54
EV_QUEUE_DEL = 0x55
EV_QUEUE_MOVE = 0x56
EV_QUEUE_CLEAR = 0x57
