from typing import Union

from .http_client import HttpClient
from ..types import (
    PermissionInfo, PermissionId, PermissionValue, PermissionOverview,
    PermissionAssignment, PrivilegeKey, CustomProperty,
)


def _perm_key(perm: Union[int, str]) -> str:
    """An int selects ``permid``, a str selects ``permsid``."""
    return 'permid' if isinstance(perm, int) else 'permsid'


class Permission:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def _list(self, command: str, model, params=None, json_body=None):
        response = await self.http_client.request_list(command, params=params, json_body=json_body)
        return [model.from_dict(item) for item in response]

    async def permission_list(self) -> list[PermissionInfo]:
        """Lists all permissions available on the server instance (ID, name, description)."""
        return await self._list('permissionlist', PermissionInfo)

    async def perm_id_get_by_name(self, permsids: list[str]) -> list[PermissionId]:
        """
        Returns the IDs of one or more permissions.

        :param permsids: Permission names, e.g. ['i_client_poke_power'].
        """
        body = [{'permsid': permsid} for permsid in permsids]
        return await self._list('permidgetbyname', PermissionId, json_body=body)

    async def perm_overview(
            self,
            cid: int,
            cldbid: int,
            perms: list[Union[int, str]] | None = None
    ) -> list[PermissionOverview]:
        """
        Lists all permissions assigned to a client for a channel.

        :param cid: Channel ID.
        :param cldbid: Client database ID.
        :param perms: Permissions to look at; an int is a permid, a str a permsid. Defaults to
            ``[0]`` (all permissions).
        """
        perms = [0] if perms is None else perms
        body = [{'cid': cid, 'cldbid': cldbid, _perm_key(p): p} for p in perms]
        return await self._list('permoverview', PermissionOverview, json_body=body)

    async def perm_get(self, perms: list[Union[int, str]]) -> list[PermissionValue]:
        """
        Returns the current value of permissions for your own connection.

        :param perms: Permissions to check; an int is a permid, a str a permsid.
        """
        body = [{_perm_key(p): p} for p in perms]
        return await self._list('permget', PermissionValue, json_body=body)

    async def perm_find(self, perms: list[Union[int, str]]) -> list[PermissionAssignment]:
        """
        Lists all assignments of the given permissions. Returns an empty list
        if the permissions are not assigned anywhere.

        :param perms: Permissions to find; an int is a permid, a str a permsid.
        """
        body = [{_perm_key(p): p} for p in perms]
        return await self._list('permfind', PermissionAssignment, json_body=body)

    async def perm_reset(self) -> str:
        """
        Restores the default permission settings on the selected virtual server and creates a new
        initial administrator token. DESTRUCTIVE: if the call fails midway, the virtual server
        is deleted from the database.

        :return: The new administrator token.
        """
        response = await self.http_client.request('permreset')
        return str(response[0]['token'])

    async def privilege_key_list(self) -> list[PrivilegeKey]:
        """Lists the privilege keys (tokens). Returns an empty list if there are none."""
        return await self._list('privilegekeylist', PrivilegeKey)

    async def privilege_key_add(
            self,
            tokentype: int,
            tokenid1: int,
            tokenid2: int = 0,
            tokendescription: str | None = None,
            tokencustomset: str | None = None
    ) -> str:
        """
        Creates a new privilege key.

        :param tokentype: 0 = server group token, 1 = channel group token.
        :param tokenid1: The server group ID (type 0) or channel group ID (type 1).
        :param tokenid2: The channel ID (only for type 1; 0 otherwise).
        :param tokendescription: Optional description.
        :param tokencustomset: Optional escaped set of custom client properties
            (``ident=a value=b|ident=c value=d``).
        :return: The new token.
        """
        params: dict = {'tokentype': tokentype, 'tokenid1': tokenid1, 'tokenid2': tokenid2}
        if tokendescription is not None:
            params['tokendescription'] = tokendescription
        if tokencustomset is not None:
            params['tokencustomset'] = tokencustomset
        response = await self.http_client.request('privilegekeyadd', params=params)
        return str(response[0]['token'])

    async def privilege_key_delete(self, token: str) -> None:
        """Deletes a privilege key."""
        await self.http_client.request('privilegekeydelete', params={'token': token})

    async def privilege_key_use(self, token: str) -> None:
        """Uses a privilege key to gain access to a server or channel group; the key is then deleted."""
        await self.http_client.request('privilegekeyuse', params={'token': token})

    async def custom_search(self, ident: str, pattern: str) -> list[CustomProperty]:
        """
        Searches custom client properties by ident and value pattern (SQL wildcards like % allowed).
        Returns an empty list if nothing matches.
        """
        return await self._list('customsearch', CustomProperty, params={'ident': ident, 'pattern': pattern})

    async def custom_info(self, cldbid: int) -> list[CustomProperty]:
        """Lists the custom properties of a client. Returns an empty list if there are none."""
        return await self._list('custominfo', CustomProperty, params={'cldbid': cldbid})
