from typing import Union

from .http_client import HttpClient
from ..properties.channel_create import ChannelCreateProperties, ChannelEditProperties
from ..types import ChannelListInfo, ChannelInfo, ChannelFindResult, ChannelPermission


class Channel:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def channel_list(self) -> list[ChannelListInfo]:
        channels = await self.http_client.request_list('channellist')
        return [ChannelListInfo.from_dict(channel) for channel in channels]

    async def channel_info(self, cid: int) -> ChannelInfo:
        """
        Displays detailed configuration information about a channel.

        :param cid: The ID of the channel.
        :return: ChannelInfo object.
        """
        response = await self.http_client.request('channelinfo', params={'cid': cid})
        return ChannelInfo.from_dict(response[0])

    async def channel_find(self, pattern: str) -> list[ChannelFindResult]:
        """
        Displays a list of channels matching a given name pattern.

        :param pattern: The channel name pattern to search for.
        :return: List of ChannelFindResult objects.
        """
        response = await self.http_client.request_list('channelfind', params={'pattern': pattern})
        return [ChannelFindResult.from_dict(item) for item in response]

    async def channel_move(self, cid: int, cpid: int, order: int = 0) -> None:
        """
        Moves a channel to a new parent channel with the ID cpid.

        :param cid: The ID of the channel to move.
        :param cpid: The ID of the new parent channel.
        :param order: The channel will be sorted right under the channel with this ID.
            0 sorts the channel right below the new parent.
        """
        params = {'cid': cid, 'cpid': cpid, 'order': order}
        await self.http_client.request('channelmove', params=params)

    async def channel_create(self, properties: ChannelCreateProperties) -> int:
        """
        Creates a new channel using the given properties.

        :param properties: Properties of the new channel (channel_name is required).
        :return: The new channel's ID.
        """
        response = await self.http_client.request('channelcreate', params=dict(properties))
        return int(response[0]['cid'])

    async def channel_delete(self, cid: int, force: bool = False) -> None:
        """
        Deletes an existing channel by ID.

        :param cid: The ID of the channel to delete.
        :param force: If True, delete the channel even if there are clients within
            (they will be kicked to the default channel).
        """
        params = {'cid': cid, 'force': 1 if force else 0}
        await self.http_client.request('channeldelete', params=params)

    async def channel_edit(self, cid: int, properties: ChannelEditProperties) -> None:
        """
        Changes a channel's configuration using given properties.

        :param cid: The ID of the channel to edit.
        :param properties: Properties to change.
        """
        params = {'cid': cid, **properties}
        await self.http_client.request('channeledit', params=params)

    async def channel_perm_list(
            self,
            cid: int,
            permsid: bool = False
    ) -> list[ChannelPermission]:
        """
        Displays a list of permissions defined for a channel.

        :param cid: The ID of the channel.
        :param permsid: If True, return permission names (permsid) instead of numeric IDs.
        :return: List of ChannelPermission objects.
        """
        params: list | dict
        if permsid:
            params = [f'cid={cid}', '-permsid']
        else:
            params = {'cid': cid}
        response = await self.http_client.request_list('channelpermlist', params=params)
        return [ChannelPermission.from_dict(item) for item in response]

    async def channel_add_perm(self, cid: int, permissions: dict[int, int]) -> None:
        """
        Adds a set of specified permissions to a channel.

        :param cid: The ID of the channel.
        :param permissions: Mapping of permid -> permvalue. Multiple permissions can
            be added in a single call.
        """
        body = [{'cid': cid, 'permid': permid, 'permvalue': permvalue} for permid, permvalue in permissions.items()]
        await self.http_client.request('channeladdperm', json_body=body)

    async def channel_del_perm(self, cid: int, permids: list[int]) -> None:
        """
        Removes a set of specified permissions from a channel.

        :param cid: The ID of the channel.
        :param permids: List of permission IDs to remove.
        """
        body = [{'cid': cid, 'permid': permid} for permid in permids]
        await self.http_client.request('channeldelperm', json_body=body)

    async def channel_client_perm_list(
            self,
            cid: int,
            cldbid: int,
            permsid: bool = False
    ) -> list[ChannelPermission]:
        """
        Lists the permissions defined for a client in a specific channel.
        Returns an empty list if there are none.

        :param cid: The ID of the channel.
        :param cldbid: The client database ID.
        :param permsid: If True, return permission names (permsid) instead of numeric IDs.
        """
        params = [f'cid={cid}', f'cldbid={cldbid}'] + (['-permsid'] if permsid else [])
        response = await self.http_client.request_list('channelclientpermlist', params=params)
        return [ChannelPermission.from_dict(item) for item in response]

    async def channel_client_add_perm(
            self,
            cid: int,
            cldbid: int,
            permissions: list[tuple[Union[int, str], int]]
    ) -> None:
        """
        Adds permissions to a client in a specific channel.

        :param permissions: List of (perm, value) tuples; an int perm is a permid, a str a permsid.
        """
        body = [
            {'cid': cid, 'cldbid': cldbid, 'permid' if isinstance(perm, int) else 'permsid': perm,
             'permvalue': value}
            for perm, value in permissions
        ]
        await self.http_client.request('channelclientaddperm', json_body=body)

    async def channel_client_del_perm(
            self,
            cid: int,
            cldbid: int,
            perms: list[Union[int, str]]
    ) -> None:
        """
        Removes permissions from a client in a specific channel.

        :param perms: Permissions to remove; an int is a permid, a str a permsid.
        """
        body = [{'cid': cid, 'cldbid': cldbid, 'permid' if isinstance(p, int) else 'permsid': p} for p in perms]
        await self.http_client.request('channelclientdelperm', json_body=body)
