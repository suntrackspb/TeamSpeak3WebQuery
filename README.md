# ts3-web-query

[Русская версия](https://github.com/suntrackspb/TeamSpeak3WebQuery/blob/master/README_RU.md)

Async Python wrapper for the **TeamSpeak 3 HTTP WebQuery API** (not the raw telnet/SSH
ServerQuery). Built on `aiohttp`; commands return typed dataclasses.

> **Status: beta.** All ServerQuery commands accepted by WebQuery are covered
> (109 of the 130 documented ones); see [Not supported](#not-supported).

## Requirements

- Python 3.10+
- `aiohttp >= 3.9`
- A TeamSpeak 3 server with WebQuery enabled and an API key (`apikeyadd`)

## Installation

```bash
pip install ts3-web-query
```

## Quick start

```python
import asyncio
from ts3_web_query import Client


async def main():
    async with Client(
        api_url="http://127.0.0.1:10080",  # WebQuery address
        api_key="BABAB...",                 # x-api-key
        instance_id=1,                      # virtual server (sid)
        timeout=30.0,                       # total request timeout, seconds
    ) as client:
        print(await client.server.server_info())
        print(await client.channel.channel_list())


asyncio.run(main())
```

Without `async with`, close the HTTP session yourself: `await client.close()`.
A complete example is in [examples/basic_usage.py](https://github.com/suntrackspb/TeamSpeak3WebQuery/blob/master/examples/basic_usage.py).

## Types and IDE hints

```python
from ts3_web_query import Client
from ts3_web_query.constants import TargetMode
from ts3_web_query.properties import ChannelCreateProperties
from ts3_web_query.types import ServerInfo

props: ChannelCreateProperties = {"channel_name": "Lobby", "channel_flag_permanent": 1}
cid = await client.channel.channel_create(props)   # int

info = await client.server.server_info()           # ServerInfo: fields are suggested
print(info.virtualserver_name)
```

Create/edit properties are `TypedDict`s, so editors and `mypy` check the keys. The package ships `py.typed`.

## Error handling

All exceptions derive from `ts3_web_query.TeamSpeakException`:

- `TeamSpeakAPIError(code, message, extra_message)`: the server answered with an error, e.g.
  `2568 insufficient client permissions (failed_permid=17)`.
- `TeamSpeakConnectionError`: the HTTP request failed, timed out, or the response had an unexpected format.

```python
from ts3_web_query import TeamSpeakAPIError

try:
    await client.channel.channel_delete(cid=5, force=True)
except TeamSpeakAPIError as exc:
    print("failed:", exc.code, exc.message)
```

Commands without a payload return `None`. An empty result is an empty list, not an error:
TeamSpeak reports it as error 1281 (`database empty result set`), which the library maps to `[]`
for every method that returns a list (`ban_list()` with no bans returns `[]`).

## Implemented API

| Area | `Client` attribute | Methods |
|---|---|---|
| Server / instance | `client.server` | `server_list`, `server_info`, `server_id_get_by_port`, `server_create`, `server_edit`, `server_delete`, `server_start`, `server_stop`, `server_process_stop`, `server_request_connection_info`, `server_temp_password_add/del/list`, `host_info`, `whoami`, `version`, `instance_info`, `instance_edit`, `log_view`, `log_add`, `global_message`, `server_snapshot_create`, `server_snapshot_deploy` |
| Channels | `client.channel` | `channel_list`, `channel_info`, `channel_find`, `channel_create`, `channel_edit`, `channel_move`, `channel_delete`, `channel_perm_list`, `channel_add_perm`, `channel_del_perm`, `channel_client_perm_list`, `channel_client_add_perm`, `channel_client_del_perm` |
| Channel groups | `client.channel_group` | `channel_group_list`, `channel_group_add`, `channel_group_del`, `channel_group_copy`, `channel_group_rename`, `channel_group_perm_list`, `channel_group_add_perm`, `channel_group_del_perm`, `channel_group_client_list`, `set_client_channel_group` |
| Server groups | `client.server_group` | `server_groups_list`, `server_group_add`, `server_group_del`, `server_group_copy`, `server_group_rename`, `server_group_perm_list`, `server_group_add_perm`, `server_group_del_perm`, `server_group_add_client`, `server_group_del_client`, `server_group_client_list`, `server_groups_by_client_id`, `server_group_auto_add_perm`, `server_group_auto_del_perm` |
| Clients | `client.clients` | `client_list`, `client_info`, `client_find`, `client_edit`, `client_update`, `client_move`, `client_kick`, `client_poke`, `client_db_list`, `client_db_info`, `client_db_find`, `client_db_edit`, `client_db_delete`, `client_get_ids`, `client_get_dbid_from_uid`, `client_get_name_from_uid`, `client_get_uid_from_clid`, `client_get_name_from_dbid`, `client_set_serverquery_login`, `client_perm_list`, `client_add_perm`, `client_del_perm` |
| Permissions / tokens | `client.permission` | `permission_list`, `perm_id_get_by_name`, `perm_overview`, `perm_get`, `perm_find`, `perm_reset`, `privilege_key_list/add/delete/use`, `custom_search`, `custom_info` |
| Messages, complaints, bans | `client.messaging` | `send_text_message`, `send_private_message`, `message_list/add/del/get/update_flag`, `complain_list/add/del/del_all`, `ban_client`, `ban_list`, `ban_add`, `ban_del`, `ban_del_all` |

Methods with repeated parameters (several `clid`s, permission sets, ...) take lists. They are
sent as POST with a JSON body, because WebQuery silently honors only the first value of a
repeated query-string key.

Some operations are destructive: `perm_reset` resets the virtual server's permissions,
`server_snapshot_deploy` recreates channels and groups (their IDs change), `ban_del_all`
removes every ban.

## Limitations

- `server_create` is limited by the server license (a second virtual server gives error 2816 without one).
- `client_set_serverquery_login` does not work over WebQuery: a connection authorized by an API key has no client ID (error 512).
- Commands of the whole instance (`serverlist`, `servercreate`, `serverdelete`, `serverstart`, `serverstop`, `hostinfo`, `version`, ...) are sent without a virtual server ID in the path; every other command uses `instance_id`.

## Not supported

- File transfer (`ft*`, 9 commands): WebQuery answers `5120 out of scope` for any API key.
- `servernotifyregister` / `servernotifyunregister`: unavailable in WebQuery.
- Raw-session commands `login`, `logout`, `use`, `quit`, `help`, `bindinglist`: authentication
  uses the `x-api-key` header and the server is chosen with `instance_id`.
- Aliases `tokenadd/tokendelete/tokenlist/tokenuse`: use `privilege_key_*`.

## License

[MIT](https://github.com/suntrackspb/TeamSpeak3WebQuery/blob/master/LICENSE)
