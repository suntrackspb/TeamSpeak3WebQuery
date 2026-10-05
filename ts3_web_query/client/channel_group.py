
from .http_client import HttpClient
from ..constants import GroupType
from ..types import ChannelGroupList, ChannelGroupClient
from ..types.channel import ChannelPermission


class ChannelGroup:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def channel_group_list(self) -> list[ChannelGroupList]:
        groups = await self.http_client.request_list('channelgrouplist')
        return [ChannelGroupList.from_dict(channel_group) for channel_group in groups if
                int(channel_group['type']) == GroupType.REGULAR]

    async def channel_group_add(self, name: str, group_type: int = GroupType.REGULAR) -> int:
        """
        Creates a new channel group using a given name.

        :param name: The name of the new channel group.
        :param group_type: The group database type (see GroupType). Defaults to a regular group.
        :return: The new channel group's ID.
        """
        response = await self.http_client.request('channelgroupadd', params={'name': name, 'type': group_type})
        return int(response[0]['cgid'])

    async def channel_group_del(self, cgid: int, force: bool = False) -> None:
        """
        Deletes a channel group by ID.

        :param cgid: The ID of the channel group to delete.
        :param force: If True, delete the group even if clients are assigned to it.
        """
        params = {'cgid': cgid, 'force': 1 if force else 0}
        await self.http_client.request('channelgroupdel', params=params)

    async def channel_group_copy(
            self,
            scgid: int,
            name: str,
            tcgid: int = 0,
            group_type: int = GroupType.REGULAR
    ) -> int:
        """
        Creates a copy of the channel group specified with scgid.

        :param scgid: The ID of the source channel group.
        :param name: Name for the new group. Ignored if tcgid targets an existing group.
        :param tcgid: Target group ID. 0 creates a new group.
        :param group_type: The group database type (see GroupType).
        :return: The resulting channel group's ID.
        """
        params = {'scgid': scgid, 'tcgid': tcgid, 'name': name, 'type': group_type}
        response = await self.http_client.request('channelgroupcopy', params=params)
        return int(response[0]['cgid'])

    async def channel_group_rename(self, cgid: int, name: str) -> None:
        """
        Changes the name of a specified channel group.

        :param cgid: The ID of the channel group.
        :param name: The new name.
        """
        await self.http_client.request('channelgrouprename', params={'cgid': cgid, 'name': name})

    async def channel_group_perm_list(
            self,
            cgid: int,
            permsid: bool = False
    ) -> list[ChannelPermission]:
        """
        Displays a list of permissions assigned to the channel group specified with cgid.

        :param cgid: The ID of the channel group.
        :param permsid: If True, return permission names (permsid) instead of numeric IDs.
        :return: List of ChannelPermission objects.
        """
        params: list | dict
        if permsid:
            params = [f'cgid={cgid}', '-permsid']
        else:
            params = {'cgid': cgid}
        response = await self.http_client.request_list('channelgrouppermlist', params=params)
        return [ChannelPermission.from_dict(item) for item in response]

    async def channel_group_add_perm(self, cgid: int, permissions: dict[int, int]) -> None:
        """
        Adds a set of specified permissions to a channel group.

        :param cgid: The ID of the channel group.
        :param permissions: Mapping of permid -> permvalue.
        """
        body = [{'cgid': cgid, 'permid': permid, 'permvalue': permvalue} for permid, permvalue in permissions.items()]
        await self.http_client.request('channelgroupaddperm', json_body=body)

    async def channel_group_del_perm(self, cgid: int, permids: list[int]) -> None:
        """
        Removes a set of specified permissions from the channel group.

        :param cgid: The ID of the channel group.
        :param permids: List of permission IDs to remove.
        """
        body = [{'cgid': cgid, 'permid': permid} for permid in permids]
        await self.http_client.request('channelgroupdelperm', json_body=body)

    async def channel_group_client_list(
            self,
            cid: int | None = None,
            cldbid: int | None = None,
            cgid: int | None = None
    ) -> list[ChannelGroupClient]:
        """
        Displays all the client and/or channel IDs currently assigned to channel groups.
        All parameters are optional.

        :param cid: Filter by channel ID.
        :param cldbid: Filter by client database ID.
        :param cgid: Filter by channel group ID.
        :return: List of ChannelGroupClient objects.
        """
        params = {}
        if cid is not None:
            params['cid'] = cid
        if cldbid is not None:
            params['cldbid'] = cldbid
        if cgid is not None:
            params['cgid'] = cgid
        response = await self.http_client.request_list('channelgroupclientlist', params=params)
        return [ChannelGroupClient.from_dict(item) for item in response]

    async def set_client_channel_group(self, cgid: int, cid: int, cldbid: int) -> None:
        """
        Sets the channel group of a client to the ID specified with cgid.

        :param cgid: The ID of the channel group to assign.
        :param cid: The ID of the channel.
        :param cldbid: The client database ID.
        """
        params = {'cgid': cgid, 'cid': cid, 'cldbid': cldbid}
        await self.http_client.request('setclientchannelgroup', params=params)
