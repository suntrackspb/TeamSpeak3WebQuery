
from .http_client import HttpClient
from ..constants import GroupType
from ..types import ServerGroupList, ServerGroupClient, ServerGroupByClient
from ..types.channel import ChannelPermission


class ServerGroup:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def server_groups_list(self) -> list[ServerGroupList]:
        server_groups = await self.http_client.request_list('servergrouplist')
        return [ServerGroupList.from_dict(server_group) for server_group in server_groups if
                int(server_group['type']) == GroupType.REGULAR]

    async def server_group_add(self, name: str, group_type: int = GroupType.REGULAR) -> int:
        """
        Creates a new server group using a given name.

        :param name: The name of the new server group.
        :param group_type: The group database type (see GroupType). Defaults to a regular group.
        :return: The new server group's ID.
        """
        response = await self.http_client.request('servergroupadd', params={'name': name, 'type': group_type})
        return int(response[0]['sgid'])

    async def server_group_del(self, sgid: int, force: bool = False) -> None:
        """
        Deletes a server group by ID.

        :param sgid: The ID of the server group to delete.
        :param force: If True, delete the group even if clients are assigned to it.
        """
        params = {'sgid': sgid, 'force': 1 if force else 0}
        await self.http_client.request('servergroupdel', params=params)

    async def server_group_copy(
            self,
            ssgid: int,
            name: str,
            tsgid: int = 0,
            group_type: int = GroupType.REGULAR
    ) -> int:
        """
        Creates a copy of the server group specified with ssgid.

        :param ssgid: The ID of the source server group.
        :param name: Name for the new group. Ignored if tsgid targets an existing group.
        :param tsgid: Target group ID. 0 creates a new group.
        :param group_type: The group database type (see GroupType).
        :return: The resulting server group's ID.
        """
        params = {'ssgid': ssgid, 'tsgid': tsgid, 'name': name, 'type': group_type}
        response = await self.http_client.request('servergroupcopy', params=params)
        return int(response[0]['sgid'])

    async def server_group_rename(self, sgid: int, name: str) -> None:
        """
        Changes the name of a specified server group.

        :param sgid: The ID of the server group.
        :param name: The new name.
        """
        await self.http_client.request('servergrouprename', params={'sgid': sgid, 'name': name})

    async def server_group_perm_list(
            self,
            sgid: int,
            permsid: bool = False
    ) -> list[ChannelPermission]:
        """
        Displays a list of permissions assigned to the server group specified with sgid.

        :param sgid: The ID of the server group.
        :param permsid: If True, return permission names (permsid) instead of numeric IDs.
        :return: List of ChannelPermission objects.
        """
        params: list | dict
        if permsid:
            params = [f'sgid={sgid}', '-permsid']
        else:
            params = {'sgid': sgid}
        response = await self.http_client.request_list('servergrouppermlist', params=params)
        return [ChannelPermission.from_dict(item) for item in response]

    async def server_group_add_perm(self, sgid: int, permissions: dict[int, int]) -> None:
        """
        Adds a set of specified permissions to a server group.

        :param sgid: The ID of the server group.
        :param permissions: Mapping of permid -> permvalue.
        """
        body = [
            {'sgid': sgid, 'permid': permid, 'permvalue': permvalue, 'permnegated': 0, 'permskip': 0}
            for permid, permvalue in permissions.items()
        ]
        await self.http_client.request('servergroupaddperm', json_body=body)

    async def server_group_del_perm(self, sgid: int, permids: list[int]) -> None:
        """
        Removes a set of specified permissions from the server group.

        :param sgid: The ID of the server group.
        :param permids: List of permission IDs to remove.
        """
        body = [{'sgid': sgid, 'permid': permid} for permid in permids]
        await self.http_client.request('servergroupdelperm', json_body=body)

    async def server_group_add_client(self, sgid: int, cldbid: int) -> None:
        """
        Adds a client to the server group specified with sgid.

        :param sgid: The ID of the server group.
        :param cldbid: The client database ID.
        """
        params = {'sgid': sgid, 'cldbid': cldbid}
        await self.http_client.request('servergroupaddclient', params=params)

    async def server_group_del_client(self, sgid: int, cldbid: int) -> None:
        """
        Removes a client from the server group specified with sgid.

        :param sgid: The ID of the server group.
        :param cldbid: The client database ID.
        """
        params = {'sgid': sgid, 'cldbid': cldbid}
        await self.http_client.request('servergroupdelclient', params=params)

    async def server_group_client_list(
            self,
            sgid: int,
            names: bool = False
    ) -> list[ServerGroupClient]:
        """
        Displays the IDs of all clients currently residing in the server group specified with sgid.

        :param sgid: The ID of the server group.
        :param names: If True, also include nickname and unique identifier of the clients.
        :return: List of ServerGroupClient objects.
        """
        params: list | dict
        if names:
            params = [f'sgid={sgid}', '-names']
        else:
            params = {'sgid': sgid}
        response = await self.http_client.request_list('servergroupclientlist', params=params)
        return [ServerGroupClient.from_dict(item) for item in response]

    async def server_groups_by_client_id(self, cldbid: int) -> list[ServerGroupByClient]:
        """
        Displays all server groups the client specified with cldbid is currently residing in.

        :param cldbid: The client database ID.
        :return: List of ServerGroupByClient objects.
        """
        response = await self.http_client.request_list('servergroupsbyclientid', params={'cldbid': cldbid})
        return [ServerGroupByClient.from_dict(item) for item in response]

    async def server_group_auto_add_perm(self, sgtype: int, permissions: dict[int, int]) -> None:
        """
        Adds a set of specified permissions to *ALL* regular server groups on all virtual
        servers. The target groups are identified by the value of their
        i_group_auto_update_type permission specified with sgtype.

        :param sgtype: The i_group_auto_update_type value identifying the target groups.
        :param permissions: Mapping of permid -> permvalue.
        """
        body = [
            {'sgtype': sgtype, 'permid': permid, 'permvalue': permvalue, 'permnegated': 0, 'permskip': 0}
            for permid, permvalue in permissions.items()
        ]
        await self.http_client.request('servergroupautoaddperm', json_body=body)

    async def server_group_auto_del_perm(self, sgtype: int, permids: list[int]) -> None:
        """
        Removes a set of specified permissions from *ALL* regular server groups on all
        virtual servers. The target groups are identified by the value of their
        i_group_auto_update_type permission specified with sgtype.

        :param sgtype: The i_group_auto_update_type value identifying the target groups.
        :param permids: List of permission IDs to remove.
        """
        body = [{'sgtype': sgtype, 'permid': permid} for permid in permids]
        await self.http_client.request('servergroupautodelperm', json_body=body)
