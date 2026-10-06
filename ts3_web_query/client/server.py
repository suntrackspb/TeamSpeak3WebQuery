
from typing import Literal, overload

from .http_client import HttpClient
from ..properties.server_create import (
    ServerCreateProperties, ServerCreateResponse, ServerEditProperties, InstanceEditProperties,
)
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
    ) -> list[ServerListItem]:
        """
        Displays a list of virtual servers including their ID, status, number of clients online, etc.

        :param _all: If True, list all virtual servers stored in the database.
        :param only_offline: If True, list only offline servers.
        :return: List of ServerList objects.
        """
        params = []
        if _all:
            params.append('-all')
        if only_offline:
            params.append('-onlyoffline')
        server_list = await self.http_client.request_list('serverlist', instance_level=True, params=params)
        return [ServerListItem.from_dict(server) for server in server_list]

    async def server_info(self) -> ServerInfo:
        """
        Displays detailed configuration information about the selected virtual server.

        :return: ServerInfo object.
        """
        server_info = await self.http_client.request('serverinfo')
        return ServerInfo.from_dict(server_info[0])

    async def server_id_get_by_port(self, port: int) -> int:
        """
        Displays the database ID of the virtual server running on the specified UDP port.

        :param port: The UDP port of the virtual server.
        :return: Server ID.
        """
        response = await self.http_client.request('serveridgetbyport', instance_level=True, params={'virtualserver_port': port})
        return int(response[0]['server_id'])

    async def server_delete(self, server_id: int) -> None:
        """
        Deletes the virtual server specified with server_id.

        :param server_id: The ID of the server to delete.
        """
        await self.http_client.request('serverdelete', instance_level=True, params={'sid': server_id})

    async def server_create(self, properties: ServerCreateProperties) -> ServerCreateResponse:
        """
        Creates a new virtual server with the given name and properties.

        :param name: The name of the new virtual server.
        :param properties: Optional properties for the server.
        :return: A dictionary with server details.
        """
        params: dict = {}
        if properties:
            params.update(properties)
        response = await self.http_client.request('servercreate', instance_level=True, params=params)
        return ServerCreateResponse.from_dict(response[0])

    async def server_start(self, server_id: int) -> None:
        """
        Starts the virtual server specified with server_id.

        :param server_id: The ID of the server to start.
        """
        await self.http_client.request('serverstart', instance_level=True, params={'sid': server_id})

    async def server_stop(self, server_id: int) -> None:
        """
        Stops the virtual server specified with server_id.

        :param server_id: The ID of the server to stop.
        """
        await self.http_client.request('serverstop', instance_level=True, params={'sid': server_id})

    async def server_process_stop(self) -> None:
        """
        Stops the entire TeamSpeak 3 Server instance by shutting down the process.
        """
        await self.http_client.request('serverprocessstop', instance_level=True)

    async def server_request_connection_info(self) -> ConnectionInfo:
        """
        Displays detailed connection information about the selected virtual server
        including uptime, traffic information, etc.

        :return: ConnectionInfo object.
        """
        response = await self.http_client.request('serverrequestconnectioninfo')
        return ConnectionInfo.from_dict(response[0])

    async def server_edit(self, properties: ServerEditProperties) -> None:
        """
        Changes the selected virtual server's configuration using given properties.

        :param properties: Properties to change on the selected virtual server.
        """
        await self.http_client.request('serveredit', params=dict(properties))

    async def server_temp_password_add(
            self,
            pw: str,
            desc: str,
            duration: int,
            tcid: int = 0,
            tcpw: str = ''
    ) -> None:
        """
        Sets a new temporary server password. The client connecting with this
        password will automatically join the channel specified with tcid.

        :param pw: The temporary password.
        :param desc: A description for the temporary password.
        :param duration: Validity duration of the password in seconds.
        :param tcid: The channel the client joins automatically. 0 = default channel.
        :param tcpw: Password of the target channel, if it is protected.
        """
        params = {'pw': pw, 'desc': desc, 'duration': duration, 'tcid': tcid, 'tcpw': tcpw}
        await self.http_client.request('servertemppasswordadd', params=params)

    async def server_temp_password_del(self, pw: str) -> None:
        """
        Deletes the temporary server password specified with pw.

        :param pw: The temporary password to delete.
        """
        await self.http_client.request('servertemppassworddel', params={'pw': pw})

    async def server_temp_password_list(self) -> list[ServerTempPassword]:
        """
        Returns a list of active temporary server passwords.

        :return: List of ServerTempPassword objects.
        """
        response = await self.http_client.request_list('servertemppasswordlist')
        return [ServerTempPassword.from_dict(item) for item in response]

    async def host_info(self) -> HostInfo:
        """
        Displays detailed connection information about the server instance
        including uptime, number of virtual servers online, traffic information, etc.

        :return: HostInfo object.
        """
        response = await self.http_client.request('hostinfo', instance_level=True)
        return HostInfo.from_dict(response[0])

    async def whoami(self) -> WhoAmI:
        """
        Displays information about the current ServerQuery/API connection,
        including the currently selected virtual server.

        :return: WhoAmI object.
        """
        response = await self.http_client.request('whoami')
        return WhoAmI.from_dict(response[0])

    async def instance_info(self) -> InstanceInfo:
        """
        Displays the server instance configuration (database revision, file transfer port,
        default group IDs, flood settings, ...).

        :return: InstanceInfo object.
        """
        response = await self.http_client.request('instanceinfo', instance_level=True)
        return InstanceInfo.from_dict(response[0])

    async def instance_edit(self, properties: InstanceEditProperties) -> None:
        """
        Changes the server instance configuration using the given properties.

        :param properties: Instance properties to change.
        """
        await self.http_client.request('instanceedit', instance_level=True, params=dict(properties))

    async def log_view(
            self,
            lines: int | None = None,
            reverse: bool | None = None,
            instance: bool | None = None,
            begin_pos: int | None = None
    ) -> LogView:
        """
        Displays entries from the server log.

        :param lines: Number of entries (1-100).
        :param reverse: If True, return the newest entries first.
        :param instance: If True, read the master log file instead of the virtual server log.
        :param begin_pos: File position to start reading from (see LogView.last_pos).
        :return: LogView object.
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
        return LogView.from_response(response)

    async def log_add(self, loglevel: int, logmsg: str) -> None:
        """
        Writes a custom entry into the server log.

        :param loglevel: See LogLevel (1 error, 2 warning, 3 debug, 4 info).
        :param logmsg: The log message.
        """
        await self.http_client.request('logadd', params={'loglevel': loglevel, 'logmsg': logmsg})

    async def global_message(self, msg: str) -> None:
        """
        Sends a text message to all clients on ALL virtual servers of the instance.

        :param msg: The message text.
        """
        await self.http_client.request('gm', instance_level=True, params={'msg': msg})

    async def server_snapshot_create(self) -> ServerSnapshot:
        """
        Creates a snapshot of the selected virtual server (settings, groups, channels, known
        client identities).

        :return: ServerSnapshot object.
        """
        response = await self.http_client.request('serversnapshotcreate')
        return ServerSnapshot.from_dict(response[0])

    @overload
    async def server_snapshot_deploy(self, snapshot: ServerSnapshot, mapping: Literal[False] = False) -> None: ...

    @overload
    async def server_snapshot_deploy(self, snapshot: ServerSnapshot, mapping: Literal[True]) -> list[dict]: ...

    async def server_snapshot_deploy(self, snapshot: ServerSnapshot, mapping: bool = False) -> list[dict] | None:
        """
        Restores the selected virtual server's configuration from a snapshot. The server does NOT
        check permissions while deploying, and the current channels and groups are replaced.

        :param snapshot: A snapshot returned by server_snapshot_create.
        :param mapping: If True, the server also returns the old-to-new channel/group ID mapping.
        :return: The raw mapping entries with ``mapping=True``, otherwise ``None``.
        """
        body = {'data': snapshot.data, 'version': snapshot.version}
        if mapping:
            return await self.http_client.request_list('serversnapshotdeploy', params=['-mapping'], json_body=body)
        await self.http_client.request('serversnapshotdeploy', json_body=body)
        return None

    async def version(self) -> ServerVersion:
        """
        Displays the server's version information including platform and build number.

        :return: ServerVersion object.
        """
        response = await self.http_client.request('version', instance_level=True)
        return ServerVersion.from_dict(response[0])
