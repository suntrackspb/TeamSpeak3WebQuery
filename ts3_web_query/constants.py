class ReasonId:
    """Reason for a client kick (clientkick reasonid)."""
    KICK_FROM_CHANNEL = 4
    KICK_FROM_SERVER = 5


class TargetMode:
    """Target mode for sendtextmessage."""
    CLIENT = 1
    CHANNEL = 2
    SERVER = 3


class GroupType:
    """Type of server/channel group (servergrouplist/channelgrouplist `type`)."""
    TEMPLATE = 0
    REGULAR = 1
    QUERY = 2


class LogLevel:
    """Log level for logadd."""
    ERROR = 1
    WARNING = 2
    DEBUG = 3
    INFO = 4
