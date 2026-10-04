from dataclasses import dataclass


def _int(data: dict, key: str, default: int = 0) -> int:
    value = data.get(key)
    return int(value) if value not in (None, '') else default


@dataclass
class PermissionInfo:
    """One entry of ``permissionlist``."""
    permid: int
    permname: str
    permdesc: str

    @staticmethod
    def from_dict(data: dict) -> 'PermissionInfo':
        return PermissionInfo(
            permid=_int(data, 'permid'),
            permname=str(data.get('permname', '')),
            permdesc=str(data.get('permdesc', '')),
        )


@dataclass
class PermissionId:
    """Result of ``permidgetbyname``."""
    permid: int
    permsid: str

    @staticmethod
    def from_dict(data: dict) -> 'PermissionId':
        return PermissionId(permid=_int(data, 'permid'), permsid=str(data.get('permsid', '')))


@dataclass
class PermissionValue:
    """Result of ``permget``: the current value of a permission for your own connection."""
    permid: int
    permsid: str
    permvalue: int

    @staticmethod
    def from_dict(data: dict) -> 'PermissionValue':
        return PermissionValue(
            permid=_int(data, 'permid'),
            permsid=str(data.get('permsid', '')),
            permvalue=_int(data, 'permvalue'),
        )


@dataclass
class PermissionOverview:
    """
    One entry of ``permoverview``. ``t`` is the assignment type, ``id1``/``id2`` identify
    the group, client or channel it comes from, ``p`` is the permid, ``v`` the value,
    ``n`` the negated flag and ``s`` the skip flag.
    """
    t: int
    id1: int
    id2: int
    p: int
    v: int
    n: int
    s: int

    @staticmethod
    def from_dict(data: dict) -> 'PermissionOverview':
        return PermissionOverview(
            t=_int(data, 't'), id1=_int(data, 'id1'), id2=_int(data, 'id2'),
            p=_int(data, 'p'), v=_int(data, 'v'), n=_int(data, 'n'), s=_int(data, 's'),
        )


@dataclass
class PermissionAssignment:
    """One entry of ``permfind``: where a permission is assigned (see PermissionOverview for t/id1/id2)."""
    t: int
    id1: int
    id2: int
    p: int

    @staticmethod
    def from_dict(data: dict) -> 'PermissionAssignment':
        return PermissionAssignment(t=_int(data, 't'), id1=_int(data, 'id1'), id2=_int(data, 'id2'),
                                    p=_int(data, 'p'))


@dataclass
class PrivilegeKey:
    """One entry of ``privilegekeylist``. ``token_type`` 0 = server group, 1 = channel group."""
    token: str
    token_type: int
    token_id1: int
    token_id2: int
    token_description: str
    token_customset: str
    token_created: int

    @staticmethod
    def from_dict(data: dict) -> 'PrivilegeKey':
        return PrivilegeKey(
            token=str(data.get('token', '')),
            token_type=_int(data, 'token_type'),
            token_id1=_int(data, 'token_id1'),
            token_id2=_int(data, 'token_id2'),
            token_description=str(data.get('token_description', '')),
            token_customset=str(data.get('token_customset', '')),
            token_created=_int(data, 'token_created'),
        )


@dataclass
class CustomProperty:
    """One custom client property (``custominfo`` / ``customsearch``)."""
    cldbid: int
    ident: str
    value: str

    @staticmethod
    def from_dict(data: dict) -> 'CustomProperty':
        return CustomProperty(cldbid=_int(data, 'cldbid'), ident=str(data.get('ident', '')),
                              value=str(data.get('value', '')))
