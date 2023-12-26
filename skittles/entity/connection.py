import enum


class ConnectionType(enum.Enum):

    FORWARD_HTTP = 1
    FORWARD_WS = 2

    REVERSE_HTTP = 3
    REVERSE_WS = 4
