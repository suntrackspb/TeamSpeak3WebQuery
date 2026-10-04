# TeamSpeak 3 Web Query Wrapper

Асинхронная Python-обёртка над **HTTP WebQuery API** TeamSpeak 3 (не raw telnet/SSH
ServerQuery). Построена на `aiohttp`, команды возвращают типизированные dataclass-объекты.

> **Статус: в разработке.** Пакет пока не опубликован на PyPI и устанавливается только из
> исходников. Покрыты все команды ServerQuery, которые WebQuery принимает (109 из 130
> описанных в `docs/serverquery.html`); что не реализовано и почему — в разделе
> «Чего нет» ниже.

## Требования

- Python 3.10+ (в аннотациях используется синтаксис `X | Y`)
- `aiohttp ~= 3.10.5`
- `python-dotenv ~= 1.0.1` (нужен только примерам из `examples/`)
- Включённый WebQuery на сервере TeamSpeak 3 и API-ключ (`apikeyadd`)

## Установка

```bash
git clone https://github.com/suntrackspb/TeamSpeak3WebQuery.git
cd TeamSpeak3WebQuery
pip install -r requirements.txt
```

`pyproject.toml` / `setup.py` в репозитории пока пустые, поэтому `pip install .` не работает —
используйте каталог проекта как рабочий (или добавьте его в `PYTHONPATH`).

## Быстрый старт

```python
import asyncio
from ts3_web_query.client import Client


async def main():
    async with Client(
        api_url="http://127.0.0.1:10080",  # адрес WebQuery
        api_key="BABAB...",                 # x-api-key
        instance_id=1,                      # виртуальный сервер (sid)
    ) as client:
        print(await client.server.server_info())
        print(await client.channel.channel_list())


asyncio.run(main())
```

`Client` можно использовать и без `async with` — тогда HTTP-сессию нужно закрыть вручную
через `await client.close()`. Виртуальный сервер переключается на лету:
`client.http_client.instance_id = 2`.

Готовый пример с чтением `TS3_API_URL` / `TS3_API_KEY` из `.env` — в
[examples/basic_usage.py](examples/basic_usage.py).

## Обработка ошибок

- Сетевые сбои и неожиданный формат ответа поднимают
  `ts3_web_query.exceptions.TeamSpeakConnectionError`.
- Ошибки самого TeamSpeak **не выбрасываются**: метод возвращает
  `TeamSpeakError(code, message, extra_message)`. Команды без возвращаемого значения при
  успехе отдают `TeamSpeakError(code=0, message='ok')`.

```python
result = await client.channel.channel_delete(cid=5, force=True)
if result.code != 0:
    print("не удалось:", result.message)
```

## Что реализовано

| Раздел | Атрибут `Client` | Методы |
|---|---|---|
| Виртуальные серверы и инстанс | `client.server` | `server_list`, `server_info`, `server_id_get_by_port`, `server_create`, `server_edit`, `server_delete`, `server_start`, `server_stop`, `server_process_stop`, `server_request_connection_info`, `server_temp_password_add/del/list`, `host_info`, `whoami`, `version`, `instance_info`, `instance_edit`, `log_view`, `log_add`, `global_message`, `server_snapshot_create`, `server_snapshot_deploy` |
| Каналы | `client.channel` | `channel_list`, `channel_info`, `channel_find`, `channel_create`, `channel_edit`, `channel_move`, `channel_delete`, `channel_perm_list`, `channel_add_perm`, `channel_del_perm`, `channel_client_perm_list`, `channel_client_add_perm`, `channel_client_del_perm` |
| Группы каналов | `client.channel_group` | `channel_group_list`, `channel_group_add`, `channel_group_del`, `channel_group_copy`, `channel_group_rename`, `channel_group_perm_list`, `channel_group_add_perm`, `channel_group_del_perm`, `channel_group_client_list`, `set_client_channel_group` |
| Группы сервера | `client.server_group` | `server_groups_list`, `server_group_add`, `server_group_del`, `server_group_copy`, `server_group_rename`, `server_group_perm_list`, `server_group_add_perm`, `server_group_del_perm`, `server_group_add_client`, `server_group_del_client`, `server_group_client_list`, `server_groups_by_client_id`, `server_group_auto_add_perm`, `server_group_auto_del_perm` |
| Клиенты | `client.clients` | `client_list`, `client_info`, `client_find`, `client_edit`, `client_update`, `client_move`, `client_kick`, `client_poke`, `client_db_list`, `client_db_info`, `client_db_find`, `client_db_edit`, `client_db_delete`, `client_get_ids`, `client_get_dbid_from_uid`, `client_get_name_from_uid`, `client_get_uid_from_clid`, `client_get_name_from_dbid`, `client_set_serverquery_login`, `client_perm_list`, `client_add_perm`, `client_del_perm` |
| Права и токены | `client.permission` | `permission_list`, `perm_id_get_by_name`, `perm_overview`, `perm_get`, `perm_find`, `perm_reset`, `privilege_key_list/add/delete/use`, `custom_search`, `custom_info` |
| Сообщения, жалобы, баны | `client.messaging` | `send_text_message`, `send_private_message`, `message_list/add/del/get/update_flag`, `complain_list/add/del/del_all`, `ban_client`, `ban_list`, `ban_add`, `ban_del`, `ban_del_all` |

Методы с повторяющимися параметрами (несколько `clid`, наборов прав и т. п.) принимают списки;
под капотом они уходят POST-запросом с JSON, потому что WebQuery молча применяет только первое
значение из повторяющихся ключей query-строки.

Пустой результат сервер отдаёт как ошибку 1281 (`database empty result set`), поэтому, например,
`ban_list()` без банов вернёт `TeamSpeakError(code=1281, ...)`, а не пустой список.

Некоторые операции опасны: `perm_reset` сбрасывает права виртуального сервера,
`server_snapshot_deploy` пересоздаёт каналы и группы (их ID меняются), `ban_del_all` удаляет
все баны.

## Чего нет

- Передача файлов (`ft*`, 9 команд): WebQuery отвечает `5120 out of scope` для любого
  API-ключа, поэтому `ts3_web_query/client/filetransfer.py` остаётся пустой заглушкой.
- `servernotifyregister` / `servernotifyunregister` — тоже недоступны в WebQuery (push-уведомления
  не вписываются в HTTP request/response).
- Команды raw-сессии `login`, `logout`, `use`, `quit`, `help`, `bindinglist` — не нужны:
  авторизация идёт ключом `x-api-key`, сервер выбирается через `instance_id`.
- Алиасы `tokenadd/tokendelete/tokenlist/tokenuse` — используйте `privilege_key_*`.
- Тесты и упаковка (`pyproject.toml`, публикация на PyPI).

## Структура проекта

```
ts3_web_query/
  client/          # фасад Client + HTTP-слой + группы команд (server, channel, client_management, ...)
  types/           # dataclass-модели ответов
  properties/      # TypedDict-наборы свойств для create/edit
  constants.py     # ReasonId, TargetMode, GroupType, LogLevel
  exceptions.py    # TeamSpeakAPIError, TeamSpeakConnectionError
  utils.py         # build_request, status_to_error
docs/serverquery.html  # официальный референс ServerQuery
examples/basic_usage.py
```

Особенности HTTP API относительно raw ServerQuery (авторизация через `x-api-key` вместо
`login`/`use`, отсутствие экранирования, multi-value параметры через POST JSON) описаны в
`.claude/IMPLEMENTATION_PLAN.md`.

## Лицензия

[GNU GPL v3](LICENSE)
