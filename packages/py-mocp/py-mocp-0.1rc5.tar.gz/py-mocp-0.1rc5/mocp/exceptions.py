"""
Global mocp exceptions classes.
"""


class MocError(Exception):
    """The base exception class for MocClient."""
    pass


class MocServerBusy(MocError):
    """The server is busy; too many other clients are connected!"""
    pass


class MocServerExited(MocError):
    """The server exited!"""
    pass


class MocSocketError(Exception):
    """The base exception class for MocSocketClient."""
    pass


class MocSocketConnectionError(MocSocketError):
    """Can't establish connection."""
    pass


class MocSocketIOError(MocSocketError):
    """Input/Output error."""
    pass
