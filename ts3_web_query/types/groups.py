from dataclasses import dataclass


@dataclass
class GroupBase:
    iconid: int
    n_member_addp: int
    n_member_removep: int
    n_modifyp: int
    name: str
    namemode: int
    savedb: int
    sortid: int
    type: int


@dataclass
class ServerGroupList(GroupBase):
    sgid: int

    @staticmethod
    def from_dict(data: dict) -> 'ServerGroupList':
        return ServerGroupList(
            sgid=int(data['sgid']),
            iconid=int(data['iconid']),
            n_member_addp=int(data['n_member_addp']),
            n_member_removep=int(data['n_member_removep']),
            n_modifyp=int(data['n_modifyp']),
            name=data['name'],
            namemode=int(data['namemode']),
            savedb=int(data['savedb']),
            sortid=int(data['sortid']),
            type=int(data['type']),
        )


@dataclass
class ChannelGroupList(GroupBase):
    cgid: int

    @staticmethod
    def from_dict(data: dict) -> 'ChannelGroupList':
        return ChannelGroupList(
            cgid=int(data['cgid']),
            iconid=int(data['iconid']),
            n_member_addp=int(data['n_member_addp']),
            n_member_removep=int(data['n_member_removep']),
            n_modifyp=int(data['n_modifyp']),
            name=data['name'],
            namemode=int(data['namemode']),
            savedb=int(data['savedb']),
            sortid=int(data['sortid']),
            type=int(data['type']),
        )


@dataclass
class ChannelGroupClient:
    cid: int
    cldbid: int
    cgid: int

    @staticmethod
    def from_dict(data: dict) -> 'ChannelGroupClient':
        return ChannelGroupClient(
            cid=int(data.get('cid', 0)),
            cldbid=int(data.get('cldbid', 0)),
            cgid=int(data.get('cgid', 0)),
        )


@dataclass
class ServerGroupClient:
    cldbid: int
    client_nickname: str | None = None
    client_unique_identifier: str | None = None

    @staticmethod
    def from_dict(data: dict) -> 'ServerGroupClient':
        return ServerGroupClient(
            cldbid=int(data.get('cldbid', 0)),
            client_nickname=data.get('client_nickname'),
            client_unique_identifier=data.get('client_unique_identifier'),
        )


@dataclass
class ServerGroupByClient:
    name: str
    sgid: int
    cldbid: int

    @staticmethod
    def from_dict(data: dict) -> 'ServerGroupByClient':
        return ServerGroupByClient(
            name=data['name'],
            sgid=int(data['sgid']),
            cldbid=int(data['cldbid']),
        )