# ts3-web-query

[Русская версия](README_RU.md)

Async Python wrapper for the **TeamSpeak 3 HTTP WebQuery API** (not the raw telnet/SSH
ServerQuery). Built on `aiohttp`; commands return typed dataclasses.

> **Status: alpha.** All ServerQuery commands accepted by WebQuery are covered
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
A complete example is in [examples/basic_usage.py](examples/basic_usage.py).

## Error handling

- Network failures and unexpected responses raise `ts3_web_query.TeamSpeakConnectionError`.
- TeamSpeak errors are **not raised**: the method returns
  `TeamSpeakError(code, message, extra_message)`. Commands without a payload return
  `TeamSpeakError(code=0, message='ok')` on success.

```python
result = await client.channel.channel_delete(cid=5, force=True)
if result.code != 0:
    print("failed:", result.message)
```

An empty result is reported by the server as error 1281 (`database empty result set`),
so e.g. `ban_list()` with no bans returns `TeamSpeakError(code=1281, ...)`, not an empty list.

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

## Not supported

- File transfer (`ft*`, 9 commands): WebQuery answers `5120 out of scope` for any API key.
- `servernotifyregister` / `servernotifyunregister`: unavailable in WebQuery.
- Raw-session commands `login`, `logout`, `use`, `quit`, `help`, `bindinglist`: authentication
  uses the `x-api-key` header and the server is chosen with `instance_id`.
- Aliases `tokenadd/tokendelete/tokenlist/tokenuse`: use `privilege_key_*`.

## License

[MIT](LICENSE)
