# TeamSpeak 3 Web Query Wrapper

Асинхронная Python-обёртка над **HTTP WebQuery API** TeamSpeak 3 (не raw telnet/SSH
ServerQuery). Построена на `aiohttp`, команды возвращают типизированные dataclass-объекты.

> **Статус: в разработке.** Пакет пока не опубликован на PyPI и устанавливается только из
> исходников. Реализованная часть API перечислена ниже — остальное ещё не написано.

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

| Раздел | Атрибут `Client` | Команды |
|---|---|---|
| Виртуальные серверы | `client.server` | `server_list`, `server_info`, `server_id_get_by_port`, `server_create`, `server_edit`, `server_delete`, `server_start`, `server_stop`, `server_process_stop`, `server_request_connection_info`, `server_temp_password_add/del/list`, `host_info`, `whoami` |
| Каналы | `client.channel` | `channel_list`, `channel_info`, `channel_find`, `channel_create`, `channel_edit`, `channel_move`, `channel_delete`, `channel_perm_list`, `channel_add_perm`, `channel_del_perm` |
| Группы каналов | `client.channel_group` | `channel_group_list`, `channel_group_add`, `channel_group_del`, `channel_group_copy`, `channel_group_rename`, `channel_group_perm_list`, `channel_group_add_perm`, `channel_group_del_perm`, `channel_group_client_list`, `set_client_channel_group` |
| Группы сервера | `client.server_group` | `server_groups_list` (остальные команды группы — в работе) |

## Чего ещё нет

- Команды клиентов (`clientlist`, `clientinfo`, `clientkick`, `clientmove`, …)
- Сообщения и офлайн-почта (`ts3_web_query/client/messaging.py` — заготовка)
- Права (`ts3_web_query/client/permission.py` — заготовка)
- Передача файлов (`ts3_web_query/client/filetransfer.py` — заготовка)
- Баны, логи, снапшоты
- Тесты и упаковка (`pyproject.toml`, публикация на PyPI)

Пустые модули `permission`, `messaging`, `filetransfer` пока не подключены к фасаду `Client`.

## Структура проекта

```
ts3_web_query/
  client/          # фасад Client + HTTP-слой + группы команд
  types/           # dataclass-модели ответов
  properties/      # TypedDict-наборы свойств для create/edit
  constants.py     # ReasonId, TargetMode, GroupType
  exceptions.py    # TeamSpeakAPIError, TeamSpeakConnectionError
  utils.py         # build_request, status_to_error
docs/serverquery.html  # официальный референс ServerQuery
examples/basic_usage.py
```

Особенности HTTP API относительно raw ServerQuery (авторизация через `x-api-key` вместо
`login`/`use`, отсутствие экранирования, повторяющиеся ключи параметров) описаны в
`.claude/IMPLEMENTATION_PLAN.md`.

## Лицензия

[GNU GPL v3](LICENSE)
