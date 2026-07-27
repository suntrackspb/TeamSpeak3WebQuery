from typing import List, Union

from . import HttpClient
from ..properties.channel_create import ChannelCreateProperties, ChannelEditProperties
from ..utils import status_to_error
from ..types import ChannelListInfo, ChannelInfo, ChannelFindResult, ChannelPermission, TeamSpeakError


class Channel:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def channel_list(self) -> Union[List[ChannelListInfo], TeamSpeakError]:
        channels = await self.http_client.request('channellist')
        if isinstance(channels, list):
            return [ChannelListInfo.from_dict(channel) for channel in channels]
        else:
            return TeamSpeakError(**channels)

    async def channel_info(self, cid: int) -> Union[ChannelInfo, TeamSpeakError]:
        """
        Displays detailed configuration information about a channel.

        :param cid: The ID of the channel.
        :return: ChannelInfo object or a TeamSpeakError.
        """
        response = await self.http_client.request('channelinfo', params={'cid': cid})
        if isinstance(response, list):
            return ChannelInfo.from_dict(response[0])
        else:
            return TeamSpeakError(**response)

    async def channel_find(self, pattern: str) -> Union[List[ChannelFindResult], TeamSpeakError]:
        """
        Displays a list of channels matching a given name pattern.

        :param pattern: The channel name pattern to search for.
        :return: List of ChannelFindResult objects or a TeamSpeakError.
        """
        response = await self.http_client.request('channelfind', params={'pattern': pattern})
        if isinstance(response, list):
            return [ChannelFindResult.from_dict(item) for item in response]
        else:
            return TeamSpeakError(**response)

    async def channel_move(self, cid: int, cpid: int, order: int = 0) -> TeamSpeakError:
        """
        Moves a channel to a new parent channel with the ID cpid.

        :param cid: The ID of the channel to move.
        :param cpid: The ID of the new parent channel.
        :param order: The channel will be sorted right under the channel with this ID.
            0 sorts the channel right below the new parent.
        :return: TeamSpeakError indicating success or failure.
        """
        params = {'cid': cid, 'cpid': cpid, 'order': order}
        response = await self.http_client.request('channelmove', params=params)
        return status_to_error(response)

    async def channel_create(self, properties: ChannelCreateProperties) -> Union[int, TeamSpeakError]:
        """
        Creates a new channel using the given properties.

        :param properties: Properties of the new channel (channel_name is required).
        :return: The new channel's ID or a TeamSpeakError.
        """
        response = await self.http_client.request('channelcreate', params=dict(properties))
        if isinstance(response, list):
            return int(response[0]['cid'])
        else:
            return TeamSpeakError(**response)

    async def channel_delete(self, cid: int, force: bool = False) -> TeamSpeakError:
        """
        Deletes an existing channel by ID.

        :param cid: The ID of the channel to delete.
        :param force: If True, delete the channel even if there are clients within
            (they will be kicked to the default channel).
        :return: TeamSpeakError indicating success or failure.
        """
        params = {'cid': cid, 'force': 1 if force else 0}
        response = await self.http_client.request('channeldelete', params=params)
        return status_to_error(response)

    async def channel_edit(self, cid: int, properties: ChannelEditProperties) -> TeamSpeakError:
        """
        Changes a channel's configuration using given properties.

        :param cid: The ID of the channel to edit.
        :param properties: Properties to change.
        :return: TeamSpeakError indicating success or failure.
        """
        params = {'cid': cid, **properties}
        response = await self.http_client.request('channeledit', params=params)
        return status_to_error(response)

    async def channel_perm_list(
            self,
            cid: int,
            permsid: bool = False
    ) -> Union[List[ChannelPermission], TeamSpeakError]:
        """
        Displays a list of permissions defined for a channel.

        :param cid: The ID of the channel.
        :param permsid: If True, return permission names (permsid) instead of numeric IDs.
        :return: List of ChannelPermission objects or a TeamSpeakError.
        """
        params: list | dict
        if permsid:
            params = [f'cid={cid}', '-permsid']
        else:
            params = {'cid': cid}
        response = await self.http_client.request('channelpermlist', params=params)
        if isinstance(response, list):
            return [ChannelPermission.from_dict(item) for item in response]
        else:
            return TeamSpeakError(**response)

    async def channel_add_perm(self, cid: int, permissions: dict[int, int]) -> TeamSpeakError:
        """
        Adds a set of specified permissions to a channel.

        :param cid: The ID of the channel.
        :param permissions: Mapping of permid -> permvalue. Multiple permissions can
            be added in a single call.
        :return: TeamSpeakError indicating success or failure.
        """
        params = [f'cid={cid}']
        for permid, permvalue in permissions.items():
            params.append(f'permid={permid}')
            params.append(f'permvalue={permvalue}')
        response = await self.http_client.request('channeladdperm', params=params)
        return status_to_error(response)

    async def channel_del_perm(self, cid: int, permids: List[int]) -> TeamSpeakError:
        """
        Removes a set of specified permissions from a channel.

        :param cid: The ID of the channel.
        :param permids: List of permission IDs to remove.
        :return: TeamSpeakError indicating success or failure.
        """
        params = [f'cid={cid}'] + [f'permid={permid}' for permid in permids]
        response = await self.http_client.request('channeldelperm', params=params)
        return status_to_error(response)
