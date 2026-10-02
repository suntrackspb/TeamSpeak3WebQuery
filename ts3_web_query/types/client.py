from dataclasses import dataclass, field


def _int(data: dict, key: str, default: int = 0) -> int:
    value = data.get(key)
    return int(value) if value not in (None, '') else default


@dataclass
class ClientListItem:
    """
    One entry of ``clientlist``. Optional flags (``-uid``, ``-away``, ``-voice``, ...)
    add more keys to ``raw``; the most common ones are exposed as attributes.
    """
    clid: int
    cid: int
    client_database_id: int
    client_nickname: str
    client_type: int
    client_unique_identifier: str | None = None
    client_away: int | None = None
    client_servergroups: list[int] | None = None
    connection_client_ip: str | None = None
    raw: dict = field(default_factory=dict, repr=False)

    @staticmethod
    def from_dict(data: dict) -> 'ClientListItem':
        groups = data.get('client_servergroups')
        return ClientListItem(
            clid=_int(data, 'clid'),
            cid=_int(data, 'cid'),
            client_database_id=_int(data, 'client_database_id'),
            client_nickname=str(data.get('client_nickname', '')),
            client_type=_int(data, 'client_type'),
            client_unique_identifier=data.get('client_unique_identifier'),
            client_away=_int(data, 'client_away') if 'client_away' in data else None,
            client_servergroups=[int(g) for g in str(groups).split(',') if g] if groups is not None else None,
            connection_client_ip=data.get('connection_client_ip'),
            raw=data,
        )


@dataclass
class ClientInfo:
    """Result of ``clientinfo``. Every property returned by the server is kept in ``raw``."""
    cid: int
    client_database_id: int
    client_nickname: str
    client_type: int
    client_unique_identifier: str
    client_servergroups: list[int]
    client_channel_group_id: int
    client_away: int
    client_away_message: str
    client_description: str
    client_platform: str
    client_version: str
    client_totalconnections: int
    client_created: int
    client_lastconnected: int
    connection_client_ip: str
    raw: dict = field(default_factory=dict, repr=False)

    @staticmethod
    def from_dict(data: dict) -> 'ClientInfo':
        return ClientInfo(
            cid=_int(data, 'cid'),
            client_database_id=_int(data, 'client_database_id'),
            client_nickname=str(data.get('client_nickname', '')),
            client_type=_int(data, 'client_type'),
            client_unique_identifier=str(data.get('client_unique_identifier', '')),
            client_servergroups=[int(g) for g in str(data.get('client_servergroups', '')).split(',') if g],
            client_channel_group_id=_int(data, 'client_channel_group_id'),
            client_away=_int(data, 'client_away'),
            client_away_message=str(data.get('client_away_message', '')),
            client_description=str(data.get('client_description', '')),
            client_platform=str(data.get('client_platform', '')),
            client_version=str(data.get('client_version', '')),
            client_totalconnections=_int(data, 'client_totalconnections'),
            client_created=_int(data, 'client_created'),
            client_lastconnected=_int(data, 'client_lastconnected'),
            connection_client_ip=str(data.get('connection_client_ip', '')),
            raw=data,
        )


@dataclass
class ClientFindResult:
    clid: int
    client_nickname: str

    @staticmethod
    def from_dict(data: dict) -> 'ClientFindResult':
        return ClientFindResult(clid=_int(data, 'clid'), client_nickname=str(data.get('client_nickname', '')))


@dataclass
class ClientDbListItem:
    """One entry of ``clientdblist``."""
    cldbid: int
    client_unique_identifier: str
    client_nickname: str
    client_created: int
    client_lastconnected: int
    client_totalconnections: int
    client_description: str
    client_lastip: str
    client_login_name: str

    @staticmethod
    def from_dict(data: dict) -> 'ClientDbListItem':
        return ClientDbListItem(
            cldbid=_int(data, 'cldbid'),
            client_unique_identifier=str(data.get('client_unique_identifier', '')),
            client_nickname=str(data.get('client_nickname', '')),
            client_created=_int(data, 'client_created'),
            client_lastconnected=_int(data, 'client_lastconnected'),
            client_totalconnections=_int(data, 'client_totalconnections'),
            client_description=str(data.get('client_description', '')),
            client_lastip=str(data.get('client_lastip', '')),
            client_login_name=str(data.get('client_login_name', '')),
        )


@dataclass
class ClientDbInfo:
    """Result of ``clientdbinfo``."""
    client_database_id: int
    client_unique_identifier: str
    client_nickname: str
    client_created: int
    client_lastconnected: int
    client_totalconnections: int
    client_description: str
    client_lastip: str
    client_total_bytes_uploaded: int
    client_total_bytes_downloaded: int
    raw: dict = field(default_factory=dict, repr=False)

    @staticmethod
    def from_dict(data: dict) -> 'ClientDbInfo':
        return ClientDbInfo(
            client_database_id=_int(data, 'client_database_id'),
            client_unique_identifier=str(data.get('client_unique_identifier', '')),
            client_nickname=str(data.get('client_nickname', '')),
            client_created=_int(data, 'client_created'),
            client_lastconnected=_int(data, 'client_lastconnected'),
            client_totalconnections=_int(data, 'client_totalconnections'),
            client_description=str(data.get('client_description', '')),
            client_lastip=str(data.get('client_lastip', '')),
            client_total_bytes_uploaded=_int(data, 'client_total_bytes_uploaded'),
            client_total_bytes_downloaded=_int(data, 'client_total_bytes_downloaded'),
            raw=data,
        )


@dataclass
class ClientDbFindResult:
    cldbid: int
    client_unique_identifier: str | None = None

    @staticmethod
    def from_dict(data: dict) -> 'ClientDbFindResult':
        return ClientDbFindResult(
            cldbid=_int(data, 'cldbid'),
            client_unique_identifier=data.get('client_unique_identifier'),
        )


@dataclass
class ClientId:
    """Result of ``clientgetids``: an online client matching a unique identifier."""
    clid: int
    cluid: str
    name: str

    @staticmethod
    def from_dict(data: dict) -> 'ClientId':
        return ClientId(clid=_int(data, 'clid'), cluid=str(data.get('cluid', '')), name=str(data.get('name', '')))


@dataclass
class ClientDbName:
    """Result of ``clientgetnamefromuid`` / ``clientgetnamefromdbid``."""
    cldbid: int
    cluid: str
    name: str

    @staticmethod
    def from_dict(data: dict) -> 'ClientDbName':
        return ClientDbName(cldbid=_int(data, 'cldbid'), cluid=str(data.get('cluid', '')),
                            name=str(data.get('name', '')))


@dataclass
class ClientUid:
    """Result of ``clientgetuidfromclid``."""
    clid: int
    cluid: str
    nickname: str
    mytsid: str = ''

    @staticmethod
    def from_dict(data: dict) -> 'ClientUid':
        return ClientUid(clid=_int(data, 'clid'), cluid=str(data.get('cluid', '')),
                         nickname=str(data.get('nickname', '')), mytsid=str(data.get('mytsid', '')))
