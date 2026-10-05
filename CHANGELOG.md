# Changelog

## 0.2.0

Breaking changes:

- TeamSpeak errors are now **raised** as `TeamSpeakAPIError(code, message, extra_message)` instead of being
  returned as a `TeamSpeakError` value. Methods no longer return `Union[..., TeamSpeakError]`: they return the
  concrete type (`int`, `list[...]`, a dataclass) or `None` for commands without a payload.
- `TeamSpeakError` and `utils.status_to_error` are removed. All exceptions derive from the new
  `TeamSpeakException` (`TeamSpeakAPIError`, `TeamSpeakConnectionError`).
- An empty result of a list method is an empty list: error 1281 (`database empty result set`) and a `null` body
  are mapped to `[]` (`ban_list()`, `message_list()`, `client_db_find()`, ...).

Other changes:

- Instance-level commands (`serverlist`, `servercreate`, `serverdelete`, `serverstart`, `serverstop`,
  `serveridgetbyport`, `hostinfo`, `instanceinfo`, `instanceedit`, `version`, `gm`, `serverprocessstop`) are sent
  without a virtual server ID in the path, so `server_create` / `server_delete` work regardless of `instance_id`.
- `server_id_get_by_port` parsed the response wrongly and crashed; fixed.
- `types`, `properties` and `constants` are importable from the package root, and `ts3_web_query.properties`
  exports the TypedDict property sets for IDE completion.
- Test suite (offline, against a local fake WebQuery server) and CI on Python 3.10-3.14.

## 0.1.1

- README sections on types and limitations.

## 0.1.0

- First public release: all ServerQuery commands accepted by WebQuery (109 of 130).
