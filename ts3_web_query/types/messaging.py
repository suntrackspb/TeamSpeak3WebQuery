from dataclasses import dataclass


def _int(data: dict, key: str, default: int = 0) -> int:
    value = data.get(key)
    return int(value) if value not in (None, '') else default


@dataclass
class Message:
    """One entry of ``messagelist`` (an offline message in your inbox)."""
    msgid: int
    cluid: str
    subject: str
    timestamp: int
    flag_read: int

    @staticmethod
    def from_dict(data: dict) -> 'Message':
        return Message(
            msgid=_int(data, 'msgid'),
            cluid=str(data.get('cluid', '')),
            subject=str(data.get('subject', '')),
            timestamp=_int(data, 'timestamp'),
            flag_read=_int(data, 'flag_read'),
        )


@dataclass
class MessageContent:
    """Result of ``messageget``: an offline message including its text."""
    msgid: int
    cluid: str
    subject: str
    message: str
    timestamp: int = 0

    @staticmethod
    def from_dict(data: dict) -> 'MessageContent':
        return MessageContent(
            msgid=_int(data, 'msgid'),
            cluid=str(data.get('cluid', '')),
            subject=str(data.get('subject', '')),
            message=str(data.get('message', '')),
            timestamp=_int(data, 'timestamp'),
        )


@dataclass
class Complaint:
    """One entry of ``complainlist``: complaint about ``tcldbid`` submitted by ``fcldbid``."""
    tcldbid: int
    tname: str
    fcldbid: int
    fname: str
    message: str
    timestamp: int

    @staticmethod
    def from_dict(data: dict) -> 'Complaint':
        return Complaint(
            tcldbid=_int(data, 'tcldbid'),
            tname=str(data.get('tname', '')),
            fcldbid=_int(data, 'fcldbid'),
            fname=str(data.get('fname', '')),
            message=str(data.get('message', '')),
            timestamp=_int(data, 'timestamp'),
        )


@dataclass
class BanEntry:
    """One entry of ``banlist``. ``duration`` is in seconds, 0 means permanent."""
    banid: int
    ip: str
    name: str
    uid: str
    mytsid: str
    lastnickname: str
    created: int
    duration: int
    invokername: str
    invokercldbid: int
    invokeruid: str
    reason: str
    enforcements: int

    @staticmethod
    def from_dict(data: dict) -> 'BanEntry':
        return BanEntry(
            banid=_int(data, 'banid'),
            ip=str(data.get('ip', '')),
            name=str(data.get('name', '')),
            uid=str(data.get('uid', '')),
            mytsid=str(data.get('mytsid', '')),
            lastnickname=str(data.get('lastnickname', '')),
            created=_int(data, 'created'),
            duration=_int(data, 'duration'),
            invokername=str(data.get('invokername', '')),
            invokercldbid=_int(data, 'invokercldbid'),
            invokeruid=str(data.get('invokeruid', '')),
            reason=str(data.get('reason', '')),
            enforcements=_int(data, 'enforcements'),
        )
