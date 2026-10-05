import pytest

from ts3_web_query import TeamSpeakAPIError, TeamSpeakConnectionError
from ts3_web_query.client.http_client import HttpClient

from .conftest import fail, ok


@pytest.fixture
async def http(server):
    h = HttpClient(server.url + '/', 'k')  # trailing slash is stripped
    yield h
    await h.close()


async def test_get_sends_api_key_and_returns_body(http, server):
    server.reply('version', ok([{'version': '3.13.7'}]))
    assert await http.request('version') == [{'version': '3.13.7'}]
    assert server.last.method == 'GET'
    assert server.last.headers['x-api-key'] == 'k'


async def test_params_are_sent_in_query(http, server):
    server.reply('clientfind', ok([]))
    await http.request('clientfind', {'pattern': 'a b'})
    assert server.last.query == 'pattern=a b'  # decoded by the server


async def test_error_status_is_raised(http, server):
    server.reply('banlist', fail(2568, 'insufficient client permissions', 'failed_permid=1'))
    with pytest.raises(TeamSpeakAPIError) as exc_info:
        await http.request('banlist')
    assert (exc_info.value.code, exc_info.value.extra_message) == (2568, 'failed_permid=1')
    assert str(exc_info.value) == '2568 insufficient client permissions (failed_permid=1)'


async def test_request_list_normalises_empty_results(http, server):
    server.reply('banlist', fail(1281, 'database empty result set'))
    assert await http.request_list('banlist') == []
    server.reply('banlist', ok(None))
    assert await http.request_list('banlist') == []
    server.reply('banlist', ok([{'banid': '1'}]))
    assert await http.request_list('banlist') == [{'banid': '1'}]
    server.reply('banlist', fail(2568, 'insufficient client permissions'))
    with pytest.raises(TeamSpeakAPIError):
        await http.request_list('banlist')


def test_exception_hierarchy():
    from ts3_web_query import TeamSpeakException
    assert issubclass(TeamSpeakAPIError, TeamSpeakException)
    assert issubclass(TeamSpeakConnectionError, TeamSpeakException)


async def test_post_when_json_body_given(http, server):
    server.reply('clientmove', ok())
    await http.request('clientmove', json_body={'clid': [3, 4], 'cid': 2})
    assert server.last.method == 'POST'
    assert server.last.json == {'clid': [3, 4], 'cid': 2}


async def test_instance_id_is_part_of_url(http, server):
    server.reply('whoami', ok([]))
    http.instance_id = 3
    await http.request('whoami')
    assert server.last.sid == '3'


@pytest.mark.parametrize('bad', [0, -1, '1', None])
def test_invalid_instance_id(bad):
    h = HttpClient('http://x', 'k')
    with pytest.raises(ValueError):
        h.instance_id = bad


async def test_connection_refused_is_wrapped():
    h = HttpClient('http://127.0.0.1:1', 'k')
    try:
        with pytest.raises(TeamSpeakConnectionError):
            await h.request('version')
    finally:
        await h.close()


async def test_timeout_is_wrapped(server):
    server.reply('version', ok([]))
    server.delay = 1.0
    h = HttpClient(server.url, 'k', timeout=0.1)
    try:
        with pytest.raises(TeamSpeakConnectionError):
            await h.request('version')
    finally:
        await h.close()


@pytest.mark.parametrize('payload', [['not', 'a', 'dict'], {'no': 'status'}, {'status': 'x'}])
async def test_unexpected_format_raises(http, server, payload):
    server.reply('version', payload)
    with pytest.raises(TeamSpeakConnectionError):
        await http.request('version')


async def test_session_is_reused_and_close_is_idempotent(http, server):
    server.reply('version', ok([]))
    await http.request('version')
    session = http._client_session
    await http.request('version')
    assert http._client_session is session
    await http.close()
    await http.close()


async def test_instance_level_command_has_no_virtual_server_in_path(http, server):
    server.reply('servercreate', ok([{'sid': '2'}]))
    await http.request('servercreate', {'virtualserver_name': 'n'}, instance_level=True)
    assert (server.last.sid, server.last.command) == ('', 'servercreate')
    await http.request('servercreate', {'virtualserver_name': 'n'})
    assert server.last.sid == '1'
