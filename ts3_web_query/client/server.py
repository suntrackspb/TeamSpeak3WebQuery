from typing import Union

from .http_client import HttpClient
from ..properties.server_create import (
    ServerCreateProperties, ServerCreateResponse, ServerEditProperties, InstanceEditProperties,
)
from ..utils import status_to_error
from ..types import (
    ServerInfo,
    ServerListItem,
    ConnectionInfo,
    ServerTempPassword,
    HostInfo,
    WhoAmI,
    InstanceInfo,
    LogView,
    ServerSnapshot,
    ServerVersion,
    TeamSpeakError,
)


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
    ) -> Union[list[ServerListItem], TeamSpeakError]:
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
        server_list = await self.http_client.request('serverlist', instance_level=True, params=params)
        if isinstance(server_list, list):
            return [ServerListItem.from_dict(server) for server in server_list]
        else:
            if server_list is None:
                return []
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
        response = await self.http_client.request('serveridgetbyport', instance_level=True, params={'virtualserver_port': port})
        if isinstance(response, list):
            return int(response[0]['server_id'])
        return TeamSpeakError(**response)

    async def server_delete(self, server_id: int) -> TeamSpeakError:
        """
        Deletes the virtual server specified with server_id.

        :param server_id: The ID of the server to delete.
        :return: TeamSpeakError indicating success or failure.
        """
        response = await self.http_client.request('serverdelete', instance_level=True, params={'sid': server_id})
        return status_to_error(response)

    async def server_create(self, properties: ServerCreateProperties) -> Union[ServerCreateResponse, TeamSpeakError]:
        """
        Creates a new virtual server with the given name and properties.

        :param name: The name of the new virtual server.
        :param properties: Optional properties for the server.
        :return: A dictionary with server details or a TeamSpeakError.
        """
        params: dict = {}
        if properties:
            params.update(properties)
        response = await self.http_client.request('servercreate', instance_level=True, params=params)
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
        response = await self.http_client.request('serverstart', instance_level=True, params={'sid': server_id})
        return status_to_error(response)

    async def server_stop(self, server_id: int) -> TeamSpeakError:
        """
        Stops the virtual server specified with server_id.

        :param server_id: The ID of the server to stop.
        :return: TeamSpeakError indicating success or failure.
        """
        response = await self.http_client.request('serverstop', instance_level=True, params={'sid': server_id})
        return status_to_error(response)

    async def server_process_stop(self) -> TeamSpeakError:
        """
        Stops the entire TeamSpeak 3 Server instance by shutting down the process.

        :return: TeamSpeakError indicating success or failure.
        """
        response = await self.http_client.request('serverprocessstop', instance_level=True)
        return status_to_error(response)

    async def server_request_connection_info(self) -> Union[ConnectionInfo, TeamSpeakError]:
        """
        Displays detailed connection information about the selected virtual server
        including uptime, traffic information, etc.

        :return: ConnectionInfo object or a TeamSpeakError.
        """
        response = await self.http_client.request('serverrequestconnectioninfo')
        if isinstance(response, list):
            return ConnectionInfo.from_dict(response[0])
        else:
            return TeamSpeakError(**response)

    async def server_edit(self, properties: ServerEditProperties) -> TeamSpeakError:
        """
        Changes the selected virtual server's configuration using given properties.

        :param properties: Properties to change on the selected virtual server.
        :return: TeamSpeakError indicating success or failure.
        """
        response = await self.http_client.request('serveredit', params=dict(properties))
        return status_to_error(response)

    async def server_temp_password_add(
            self,
            pw: str,
            desc: str,
            duration: int,
            tcid: int = 0,
            tcpw: str = ''
    ) -> TeamSpeakError:
        """
        Sets a new temporary server password. The client connecting with this
        password will automatically join the channel specified with tcid.

        :param pw: The temporary password.
        :param desc: A description for the temporary password.
        :param duration: Validity duration of the password in seconds.
        :param tcid: The channel the client joins automatically. 0 = default channel.
        :param tcpw: Password of the target channel, if it is protected.
        :return: TeamSpeakError indicating success or failure.
        """
        params = {'pw': pw, 'desc': desc, 'duration': duration, 'tcid': tcid, 'tcpw': tcpw}
        response = await self.http_client.request('servertemppasswordadd', params=params)
        return status_to_error(response)

    async def server_temp_password_del(self, pw: str) -> TeamSpeakError:
        """
        Deletes the temporary server password specified with pw.

        :param pw: The temporary password to delete.
        :return: TeamSpeakError indicating success or failure.
        """
        response = await self.http_client.request('servertemppassworddel', params={'pw': pw})
        return status_to_error(response)

    async def server_temp_password_list(self) -> Union[list[ServerTempPassword], TeamSpeakError]:
        """
        Returns a list of active temporary server passwords.

        :return: List of ServerTempPassword objects or a TeamSpeakError.
        """
        response = await self.http_client.request('servertemppasswordlist')
        if isinstance(response, list):
            return [ServerTempPassword.from_dict(item) for item in response]
        else:
            if response is None:
                return []
            return TeamSpeakError(**response)

    async def host_info(self) -> Union[HostInfo, TeamSpeakError]:
        """
        Displays detailed connection information about the server instance
        including uptime, number of virtual servers online, traffic information, etc.

        :return: HostInfo object or a TeamSpeakError.
        """
        response = await self.http_client.request('hostinfo', instance_level=True)
        if isinstance(response, list):
            return HostInfo.from_dict(response[0])
        else:
            return TeamSpeakError(**response)

    async def whoami(self) -> Union[WhoAmI, TeamSpeakError]:
        """
        Displays information about the current ServerQuery/API connection,
        including the currently selected virtual server.

        :return: WhoAmI object or a TeamSpeakError.
        """
        response = await self.http_client.request('whoami')
        if isinstance(response, list):
            return WhoAmI.from_dict(response[0])
        else:
            return TeamSpeakError(**response)

    async def instance_info(self) -> Union[InstanceInfo, TeamSpeakError]:
        """
        Displays the server instance configuration (database revision, file transfer port,
        default group IDs, flood settings, ...).

        :return: InstanceInfo object or a TeamSpeakError.
        """
        response = await self.http_client.request('instanceinfo', instance_level=True)
        if isinstance(response, list):
            return InstanceInfo.from_dict(response[0])
        return TeamSpeakError(**response)

    async def instance_edit(self, properties: InstanceEditProperties) -> TeamSpeakError:
        """
        Changes the server instance configuration using the given properties.

        :param properties: Instance properties to change.
        :return: TeamSpeakError indicating success or failure.
        """
        response = await self.http_client.request('instanceedit', instance_level=True, params=dict(properties))
        return status_to_error(response)

    async def log_view(
            self,
            lines: int | None = None,
            reverse: bool | None = None,
            instance: bool | None = None,
            begin_pos: int | None = None
    ) -> Union[LogView, TeamSpeakError]:
        """
        Displays entries from the server log.

        :param lines: Number of entries (1-100).
        :param reverse: If True, return the newest entries first.
        :param instance: If True, read the master log file instead of the virtual server log.
        :param begin_pos: File position to start reading from (see LogView.last_pos).
        :return: LogView object or a TeamSpeakError.
        """
        params = {}
        if lines is not None:
            params['lines'] = lines
        if reverse is not None:
            params['reverse'] = int(reverse)
        if instance is not None:
            params['instance'] = int(instance)
        if begin_pos is not None:
            params['begin_pos'] = begin_pos
        response = await self.http_client.request('logview', params=params or None)
        if isinstance(response, list):
            return LogView.from_response(response)
        return TeamSpeakError(**response)

    async def log_add(self, loglevel: int, logmsg: str) -> TeamSpeakError:
        """
        Writes a custom entry into the server log.

        :param loglevel: See LogLevel (1 error, 2 warning, 3 debug, 4 info).
        :param logmsg: The log message.
        :return: TeamSpeakError indicating success or failure.
        """
        response = await self.http_client.request('logadd', params={'loglevel': loglevel, 'logmsg': logmsg})
        return status_to_error(response)

    async def global_message(self, msg: str) -> TeamSpeakError:
        """
        Sends a text message to all clients on ALL virtual servers of the instance.

        :param msg: The message text.
        :return: TeamSpeakError indicating success or failure.
        """
        response = await self.http_client.request('gm', instance_level=True, params={'msg': msg})
        return status_to_error(response)

    async def server_snapshot_create(self) -> Union[ServerSnapshot, TeamSpeakError]:
        """
        Creates a snapshot of the selected virtual server (settings, groups, channels, known
        client identities).

        :return: ServerSnapshot object or a TeamSpeakError.
        """
        response = await self.http_client.request('serversnapshotcreate')
        if isinstance(response, list):
            return ServerSnapshot.from_dict(response[0])
        return TeamSpeakError(**response)

    async def server_snapshot_deploy(
            self,
            snapshot: ServerSnapshot,
            mapping: bool = False
    ) -> Union[list[dict], TeamSpeakError]:
        """
        Restores the selected virtual server's configuration from a snapshot. The server does NOT
        check permissions while deploying, and the current channels and groups are replaced.

        :param snapshot: A snapshot returned by server_snapshot_create.
        :param mapping: If True, the server also returns the old-to-new channel/group ID mapping.
        :return: The raw mapping entries (empty list without mapping) or a TeamSpeakError.
        """
        body = {'data': snapshot.data, 'version': snapshot.version}
        response = await self.http_client.request(
            'serversnapshotdeploy', params=['-mapping'] if mapping else None, json_body=body)
        if response is None:
            return []
        if isinstance(response, list):
            return response
        return TeamSpeakError(**response)

    async def version(self) -> Union[ServerVersion, TeamSpeakError]:
        """
        Displays the server's version information including platform and build number.

        :return: ServerVersion object or a TeamSpeakError.
        """
        response = await self.http_client.request('version', instance_level=True)
        if isinstance(response, list):
            return ServerVersion.from_dict(response[0])
        return TeamSpeakError(**response)
