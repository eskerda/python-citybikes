import pytest_asyncio
from aiohttp import web

from citybikes.asyncio import Client

from . import mockresponses

@pytest_asyncio.fixture
async def server(aiohttp_server):
    async def networks(request):
        return web.json_response(mockresponses.networks)

    async def network(request):
        return web.json_response(mockresponses.network)

    app = web.Application()
    app.router.add_get('/v2/networks', networks)
    app.router.add_get('/v2/networks/foo', network)
    server = await aiohttp_server(app)
    yield server


@pytest_asyncio.fixture
async def client(server):
    cli = Client(endpoint=str(server.make_url('/')))
    yield cli
    await cli.close()
