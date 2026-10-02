from typing import List, Union

from . import HttpClient
from ..constants import ReasonId
from ..utils import status_to_error
from ..properties.client_edit import ClientEditProperties
from ..types import TeamSpeakError
from ..types.channel import ChannelPermission
from ..types.client import (
    ClientListItem, ClientInfo, ClientFindResult, ClientDbListItem, ClientDbInfo,
    ClientDbFindResult, ClientId, ClientDbName, ClientUid,
)

# (permid | permsid, permvalue, permskip) -- an int selects permid, a str selects permsid
ClientPermEntry = tuple[Union[int, str], int, int]


class ClientManagement:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def _list(self, command: str, model, params=None):
        response = await self.http_client.request(command, params=params)
        if isinstance(response, list):
            return [model.from_dict(item) for item in response]
        if response is None:
            return []
        return TeamSpeakError(**response)

    async def _one(self, command: str, model, params=None):
        response = await self.http_client.request(command, params=params)
        if isinstance(response, list):
            return model.from_dict(response[0])
        return TeamSpeakError(**response)

    async def client_list(self, flags: List[str] | None = None) -> Union[List[ClientListItem], TeamSpeakError]:
        """
        Lists the clients that are currently online.

        :param flags: Optional flags without dash, e.g. ['uid', 'away', 'voice', 'times', 'groups',
            'info', 'icon', 'country', 'ip'].
        :return: List of ClientListItem objects or a TeamSpeakError.
        """
        params = [f'-{flag}' for flag in flags] if flags else None
        return await self._list('clientlist', ClientListItem, params)

    async def client_info(self, clid: int) -> Union[ClientInfo, TeamSpeakError]:
        """Displays detailed configuration information about an online client."""
        return await self._one('clientinfo', ClientInfo, {'clid': clid})

    async def client_find(self, pattern: str) -> Union[List[ClientFindResult], TeamSpeakError]:
        """Finds online clients whose nickname matches the pattern."""
        return await self._list('clientfind', ClientFindResult, {'pattern': pattern})

    async def client_edit(self, clid: int, properties: ClientEditProperties) -> TeamSpeakError:
        """Changes an online client's settings using the given properties."""
        response = await self.http_client.request('clientedit', params={'clid': clid, **properties})
        return status_to_error(response)

    async def client_db_list(
            self,
            start: int | None = None,
            duration: int | None = None
    ) -> Union[List[ClientDbListItem], TeamSpeakError]:
        """
        Lists the client identities known by the server.

        :param start: Offset into the list.
        :param duration: Maximum number of entries to return.
        """
        params = {}
        if start is not None:
            params['start'] = start
        if duration is not None:
            params['duration'] = duration
        return await self._list('clientdblist', ClientDbListItem, params or None)

    async def client_db_info(self, cldbid: int) -> Union[ClientDbInfo, TeamSpeakError]:
        """Displays database information about a client."""
        return await self._one('clientdbinfo', ClientDbInfo, {'cldbid': cldbid})

    async def client_db_find(
            self,
            pattern: str,
            by_uid: bool = False
    ) -> Union[List[ClientDbFindResult], TeamSpeakError]:
        """
        Finds client database entries matching the pattern (nickname, or unique ID with by_uid).
        Returns an error with code 1281 if nothing matches.
        """
        params = [f'pattern={pattern}']
        if by_uid:
            params.append('-uid')
        return await self._list('clientdbfind', ClientDbFindResult, _quote_list(params))

    async def client_db_edit(self, cldbid: int, properties: ClientEditProperties) -> TeamSpeakError:
        """Changes a client's database settings using the given properties."""
        response = await self.http_client.request('clientdbedit', params={'cldbid': cldbid, **properties})
        return status_to_error(response)

    async def client_db_delete(self, cldbid: int) -> TeamSpeakError:
        """Deletes a client's database entry."""
        response = await self.http_client.request('clientdbdelete', params={'cldbid': cldbid})
        return status_to_error(response)

    async def client_get_ids(self, cluid: str) -> Union[List[ClientId], TeamSpeakError]:
        """Finds the online client IDs for a unique identifier."""
        return await self._list('clientgetids', ClientId, {'cluid': cluid})

    async def client_get_dbid_from_uid(self, cluid: str) -> Union[int, TeamSpeakError]:
        """Returns the database ID for a client unique identifier."""
        response = await self.http_client.request('clientgetdbidfromuid', params={'cluid': cluid})
        if isinstance(response, list):
            return int(response[0]['cldbid'])
        return TeamSpeakError(**response)

    async def client_get_name_from_uid(self, cluid: str) -> Union[ClientDbName, TeamSpeakError]:
        """Returns the last known nickname and database ID for a unique identifier."""
        return await self._one('clientgetnamefromuid', ClientDbName, {'cluid': cluid})

    async def client_get_uid_from_clid(self, clid: int) -> Union[ClientUid, TeamSpeakError]:
        """Returns the unique identifier of an online client."""
        return await self._one('clientgetuidfromclid', ClientUid, {'clid': clid})

    async def client_get_name_from_dbid(self, cldbid: int) -> Union[ClientDbName, TeamSpeakError]:
        """Returns the unique identifier and last known nickname for a database ID."""
        return await self._one('clientgetnamefromdbid', ClientDbName, {'cldbid': cldbid})

    async def client_set_serverquery_login(self, client_login_name: str) -> Union[str, TeamSpeakError]:
        """
        Updates your own ServerQuery login name; the password is auto-generated.

        :return: The generated password or a TeamSpeakError.
        """
        response = await self.http_client.request(
            'clientsetserverquerylogin', params={'client_login_name': client_login_name})
        if isinstance(response, list):
            return str(response[0]['client_login_password'])
        return TeamSpeakError(**response)

    async def client_update(self, properties: ClientEditProperties) -> TeamSpeakError:
        """Changes your own ServerQuery client's settings."""
        response = await self.http_client.request('clientupdate', params=dict(properties))
        return status_to_error(response)

    async def client_move(self, clids: List[int], cid: int, cpw: str | None = None) -> TeamSpeakError:
        """
        Moves one or more clients to a channel.

        :param clids: IDs of the clients to move.
        :param cid: Target channel ID.
        :param cpw: Channel password, if the channel has one.
        """
        body: dict = {'clid': list(clids), 'cid': cid}
        if cpw is not None:
            body['cpw'] = cpw
        response = await self.http_client.request('clientmove', json_body=body)
        return status_to_error(response)

    async def client_kick(
            self,
            clids: List[int],
            reasonid: int = ReasonId.KICK_FROM_CHANNEL,
            reasonmsg: str | None = None
    ) -> TeamSpeakError:
        """
        Kicks one or more clients from their channel or from the server.

        :param clids: IDs of the clients to kick.
        :param reasonid: ReasonId.KICK_FROM_CHANNEL or ReasonId.KICK_FROM_SERVER.
        :param reasonmsg: Optional message (max. 40 characters).
        """
        body: dict = {'clid': list(clids), 'reasonid': reasonid}
        if reasonmsg is not None:
            body['reasonmsg'] = reasonmsg
        response = await self.http_client.request('clientkick', json_body=body)
        return status_to_error(response)

    async def client_poke(self, clid: int, msg: str) -> TeamSpeakError:
        """Sends a poke message to a client."""
        response = await self.http_client.request('clientpoke', params={'clid': clid, 'msg': msg})
        return status_to_error(response)

    async def client_perm_list(
            self,
            cldbid: int,
            permsid: bool = False
    ) -> Union[List[ChannelPermission], TeamSpeakError]:
        """
        Lists the permissions defined for a client. Returns an error with code 1281 if there are none.

        :param permsid: If True, return permission names (permsid) instead of numeric IDs.
        """
        params = [f'cldbid={cldbid}'] + (['-permsid'] if permsid else [])
        return await self._list('clientpermlist', ChannelPermission, params)

    async def client_add_perm(self, cldbid: int, permissions: List[ClientPermEntry]) -> TeamSpeakError:
        """
        Adds permissions to a client.

        :param permissions: List of (perm, value, skip) tuples; an int perm is a permid, a str a permsid
        """
        body = [
            {'cldbid': cldbid, 'permid' if isinstance(perm, int) else 'permsid': perm,
             'permvalue': value, 'permskip': skip}
            for perm, value, skip in permissions
        ]
        response = await self.http_client.request('clientaddperm', json_body=body)
        return status_to_error(response)

    async def client_del_perm(self, cldbid: int, perms: List[Union[int, str]]) -> TeamSpeakError:
        """Removes permissions from a client; an int is a permid, a str a permsid."""
        body = [{'cldbid': cldbid, 'permid' if isinstance(p, int) else 'permsid': p} for p in perms]
        response = await self.http_client.request('clientdelperm', json_body=body)
        return status_to_error(response)


def _q(value) -> str:
    from urllib.parse import quote
    return quote(str(value), safe='')


def _quote_list(params: List[str]) -> List[str]:
    return [p if p.startswith('-') else f"{p.split('=', 1)[0]}={_q(p.split('=', 1)[1])}" for p in params]
