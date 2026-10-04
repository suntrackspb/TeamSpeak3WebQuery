"""Test helpers: a tiny in-process fake WebQuery server (real HTTP over localhost, no mocks of aiohttp)."""
import asyncio
from dataclasses import dataclass, field

import pytest
from aiohttp import web

from ts3_web_query import Client


def ok(body=None):
    return {'body': body, 'status': {'code': 0, 'message': 'ok'}}


def fail(code, message, extra=None):
    status = {'code': code, 'message': message}
    if extra is not None:
        status['extra_message'] = extra
    return {'status': status}


@dataclass
class Req:
    method: str
    sid: str
    command: str
    query: str
    headers: dict
    json: object = None


@dataclass
class FakeServer:
    url: str
    requests: list = field(default_factory=list)
    replies: dict = field(default_factory=dict)
    delay: float = 0.0

    def reply(self, command: str, payload) -> None:
        self.replies[command] = payload

    @property
    def last(self) -> Req:
        return self.requests[-1]


@pytest.fixture
async def server():
    fake = FakeServer(url='')

    async def handler(request: web.Request) -> web.Response:
        body = await request.json() if request.method == 'POST' else None
        command = request.match_info['command']
        fake.requests.append(Req(request.method, request.match_info['sid'], command,
                                 request.query_string, dict(request.headers), body))
        if fake.delay:
            await asyncio.sleep(fake.delay)
        return web.json_response(fake.replies.get(command, fail(256, 'command not found')))

    app = web.Application()
    app.router.add_route('*', '/{sid}/{command}', handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 0)
    await site.start()
    port = site._server.sockets[0].getsockname()[1]
    fake.url = f'http://127.0.0.1:{port}'
    yield fake
    await runner.cleanup()


@pytest.fixture
async def client(server):
    async with Client(server.url, 'secret-key', instance_id=1) as c:
        yield c
