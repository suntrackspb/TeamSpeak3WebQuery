from typing import List, Union

from . import HttpClient
from ..constants import GroupType
from ..utils import status_to_error
from ..types import ServerGroupList, ServerGroupClient, ServerGroupByClient, TeamSpeakError
from ..types.channel import ChannelPermission


class ServerGroup:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def server_groups_list(self) -> Union[List[ServerGroupList], TeamSpeakError]:
        server_groups = await self.http_client.request('servergrouplist')
        if isinstance(server_groups, list):
            return [ServerGroupList.from_dict(server_group) for server_group in server_groups if
                    int(server_group['type']) == GroupType.REGULAR]
        else:
            return TeamSpeakError(**server_groups)

    async def server_group_add(self, name: str, group_type: int = GroupType.REGULAR) -> Union[int, TeamSpeakError]:
        """
        Creates a new server group using a given name.

        :param name: The name of the new server group.
        :param group_type: The group database type (see GroupType). Defaults to a regular group.
        :return: The new server group's ID or a TeamSpeakError.
        """
        response = await self.http_client.request('servergroupadd', params={'name': name, 'type': group_type})
        if isinstance(response, list):
            return int(response[0]['sgid'])
        else:
            return TeamSpeakError(**response)

    async def server_group_del(self, sgid: int, force: bool = False) -> TeamSpeakError:
        """
        Deletes a server group by ID.

        :param sgid: The ID of the server group to delete.
        :param force: If True, delete the group even if clients are assigned to it.
        :return: TeamSpeakError indicating success or failure.
        """
        params = {'sgid': sgid, 'force': 1 if force else 0}
        response = await self.http_client.request('servergroupdel', params=params)
        return status_to_error(response)

    async def server_group_copy(
            self,
            ssgid: int,
            name: str,
            tsgid: int = 0,
            group_type: int = GroupType.REGULAR
    ) -> Union[int, TeamSpeakError]:
        """
        Creates a copy of the server group specified with ssgid.

        :param ssgid: The ID of the source server group.
        :param name: Name for the new group. Ignored if tsgid targets an existing group.
        :param tsgid: Target group ID. 0 creates a new group.
        :param group_type: The group database type (see GroupType).
        :return: The resulting server group's ID or a TeamSpeakError.
        """
        params = {'ssgid': ssgid, 'tsgid': tsgid, 'name': name, 'type': group_type}
        response = await self.http_client.request('servergroupcopy', params=params)
        if isinstance(response, list):
            return int(response[0]['sgid'])
        else:
            return TeamSpeakError(**response)

    async def server_group_rename(self, sgid: int, name: str) -> TeamSpeakError:
        """
        Changes the name of a specified server group.

        :param sgid: The ID of the server group.
        :param name: The new name.
        :return: TeamSpeakError indicating success or failure.
        """
        response = await self.http_client.request('servergrouprename', params={'sgid': sgid, 'name': name})
        return status_to_error(response)

    async def server_group_perm_list(
            self,
            sgid: int,
            permsid: bool = False
    ) -> Union[List[ChannelPermission], TeamSpeakError]:
        """
        Displays a list of permissions assigned to the server group specified with sgid.

        :param sgid: The ID of the server group.
        :param permsid: If True, return permission names (permsid) instead of numeric IDs.
        :return: List of ChannelPermission objects or a TeamSpeakError.
        """
        params: list | dict
        if permsid:
            params = [f'sgid={sgid}', '-permsid']
        else:
            params = {'sgid': sgid}
        response = await self.http_client.request('servergrouppermlist', params=params)
        if response is None:
            return []
        if isinstance(response, list):
            return [ChannelPermission.from_dict(item) for item in response]
        else:
            return TeamSpeakError(**response)

    async def server_group_add_perm(self, sgid: int, permissions: dict[int, int]) -> TeamSpeakError:
        """
        Adds a set of specified permissions to a server group.

        :param sgid: The ID of the server group.
        :param permissions: Mapping of permid -> permvalue.
        :return: TeamSpeakError indicating success or failure.
        """
        params = [f'sgid={sgid}']
        for permid, permvalue in permissions.items():
            params.append(f'permid={permid}')
            params.append(f'permvalue={permvalue}')
            params.append('permnegated=0')
            params.append('permskip=0')
        response = await self.http_client.request('servergroupaddperm', params=params)
        return status_to_error(response)

    async def server_group_del_perm(self, sgid: int, permids: List[int]) -> TeamSpeakError:
        """
        Removes a set of specified permissions from the server group.

        :param sgid: The ID of the server group.
        :param permids: List of permission IDs to remove.
        :return: TeamSpeakError indicating success or failure.
        """
        params = [f'sgid={sgid}'] + [f'permid={permid}' for permid in permids]
        response = await self.http_client.request('servergroupdelperm', params=params)
        return status_to_error(response)

    async def server_group_add_client(self, sgid: int, cldbid: int) -> TeamSpeakError:
        """
        Adds a client to the server group specified with sgid.

        :param sgid: The ID of the server group.
        :param cldbid: The client database ID.
        :return: TeamSpeakError indicating success or failure.
        """
        params = {'sgid': sgid, 'cldbid': cldbid}
        response = await self.http_client.request('servergroupaddclient', params=params)
        return status_to_error(response)

    async def server_group_del_client(self, sgid: int, cldbid: int) -> TeamSpeakError:
        """
        Removes a client from the server group specified with sgid.

        :param sgid: The ID of the server group.
        :param cldbid: The client database ID.
        :return: TeamSpeakError indicating success or failure.
        """
        params = {'sgid': sgid, 'cldbid': cldbid}
        response = await self.http_client.request('servergroupdelclient', params=params)
        return status_to_error(response)

    async def server_group_client_list(
            self,
            sgid: int,
            names: bool = False
    ) -> Union[List[ServerGroupClient], TeamSpeakError]:
        """
        Displays the IDs of all clients currently residing in the server group specified with sgid.

        :param sgid: The ID of the server group.
        :param names: If True, also include nickname and unique identifier of the clients.
        :return: List of ServerGroupClient objects or a TeamSpeakError.
        """
        params: list | dict
        if names:
            params = [f'sgid={sgid}', '-names']
        else:
            params = {'sgid': sgid}
        response = await self.http_client.request('servergroupclientlist', params=params)
        if response is None:
            return []
        if isinstance(response, list):
            return [ServerGroupClient.from_dict(item) for item in response]
        else:
            return TeamSpeakError(**response)

    async def server_groups_by_client_id(self, cldbid: int) -> Union[List[ServerGroupByClient], TeamSpeakError]:
        """
        Displays all server groups the client specified with cldbid is currently residing in.

        :param cldbid: The client database ID.
        :return: List of ServerGroupByClient objects or a TeamSpeakError.
        """
        response = await self.http_client.request('servergroupsbyclientid', params={'cldbid': cldbid})
        if response is None:
            return []
        if isinstance(response, list):
            return [ServerGroupByClient.from_dict(item) for item in response]
        else:
            return TeamSpeakError(**response)

    async def server_group_auto_add_perm(self, sgtype: int, permissions: dict[int, int]) -> TeamSpeakError:
        """
        Adds a set of specified permissions to *ALL* regular server groups on all virtual
        servers. The target groups are identified by the value of their
        i_group_auto_update_type permission specified with sgtype.

        :param sgtype: The i_group_auto_update_type value identifying the target groups.
        :param permissions: Mapping of permid -> permvalue.
        :return: TeamSpeakError indicating success or failure.
        """
        params = [f'sgtype={sgtype}']
        for permid, permvalue in permissions.items():
            params.append(f'permid={permid}')
            params.append(f'permvalue={permvalue}')
            params.append('permnegated=0')
            params.append('permskip=0')
        response = await self.http_client.request('servergroupautoaddperm', params=params)
        return status_to_error(response)

    async def server_group_auto_del_perm(self, sgtype: int, permids: List[int]) -> TeamSpeakError:
        """
        Removes a set of specified permissions from *ALL* regular server groups on all
        virtual servers. The target groups are identified by the value of their
        i_group_auto_update_type permission specified with sgtype.

        :param sgtype: The i_group_auto_update_type value identifying the target groups.
        :param permids: List of permission IDs to remove.
        :return: TeamSpeakError indicating success or failure.
        """
        params = [f'sgtype={sgtype}'] + [f'permid={permid}' for permid in permids]
        response = await self.http_client.request('servergroupautodelperm', params=params)
        return status_to_error(response)
