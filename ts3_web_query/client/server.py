from typing import List, Union, Optional

from . import HttpClient
from ..properties.server_create import ServerCreateProperties, ServerCreateResponse
from ..types import ServerInfo, ServerListItem, TeamSpeakError


class Server:
    def __init__(self, http_client: HttpClient):
        """
        Constructor for the Server class.

        :param http_client: An instance of HttpClient to use for making requests.
        """
        self.http_client = http_client

    async def server_list(
            self,
            _all: bool = False,
            only_offline: bool = False
    ) -> Union[List[ServerListItem], TeamSpeakError]:
        """
        Displays a list of virtual servers including their ID, status, number of clients online, etc.

        :param _all: If True, list all virtual servers stored in the database.
        :param only_offline: If True, list only offline servers.
        :return: List of ServerList objects or a TeamSpeakError.
        """
        params = []
        if _all:
            params.append('-all')
        if only_offline:
            params.append('-onlyoffline')
        server_list = await self.http_client.request('serverlist', params=params)
        if isinstance(server_list, list):
            return [ServerListItem.from_dict(server) for server in server_list]
        else:
            return TeamSpeakError(**server_list)

    async def server_info(self) -> Union[ServerInfo, TeamSpeakError]:
        """
        Displays detailed configuration information about the selected virtual server.

        :return: ServerInfo object or a TeamSpeakError.
        """
        server_info = await self.http_client.request('serverinfo')
        if isinstance(server_info, list):
            return ServerInfo.from_dict(server_info[0])
        else:
            return TeamSpeakError(**server_info)

    async def server_id_get_by_port(self, port: int) -> Union[int, TeamSpeakError]:
        """
        Displays the database ID of the virtual server running on the specified UDP port.

        :param port: The UDP port of the virtual server.
        :return: Server ID or a TeamSpeakError.
        """
        response = await self.http_client.request('serveridgetbyport', params={'virtualserver_port': port})
        if 'server_id' in response:
            return response['server_id']
        else:
            return TeamSpeakError(**response)

    async def server_delete(self, server_id: int) -> TeamSpeakError:
        """
        Deletes the virtual server specified with server_id.

        :param server_id: The ID of the server to delete.
        :return: TeamSpeakError indicating success or failure.
        """
        response = await self.http_client.request('serverdelete', params={'sid': server_id})
        print(response)
        return TeamSpeakError(**response)

    async def server_create(self, properties: ServerCreateProperties) -> Union[ServerCreateResponse, TeamSpeakError]:
        """
        Creates a new virtual server with the given name and properties.

        :param name: The name of the new virtual server.
        :param properties: Optional properties for the server.
        :return: A dictionary with server details or a TeamSpeakError.
        """
        params = {}
        if properties:
            params.update(properties)
        response = await self.http_client.request('servercreate', params=params)
        if isinstance(response, list):
            return ServerCreateResponse.from_dict(response[0])
        else:
            return TeamSpeakError(**response)

    async def server_start(self, server_id: int) -> TeamSpeakError:
        """
        Starts the virtual server specified with server_id.

        :param server_id: The ID of the server to start.
        :return: TeamSpeakError indicating success or failure.
        """
        response = await self.http_client.request('serverstart', params={'sid': server_id})
        return TeamSpeakError(**response)

    async def server_stop(self, server_id: int) -> TeamSpeakError:
        """
        Stops the virtual server specified with server_id.

        :param server_id: The ID of the server to stop.
        :return: TeamSpeakError indicating success or failure.
        """
        response = await self.http_client.request('serverstop', params={'sid': server_id})
        print(response)
        return TeamSpeakError(**response)

    async def server_process_stop(self) -> TeamSpeakError:
        """
        Stops the entire TeamSpeak 3 Server instance by shutting down the process.

        :return: TeamSpeakError indicating success or failure.
        """
        response = await self.http_client.request('serverprocessstop')
        return TeamSpeakError(**response)
