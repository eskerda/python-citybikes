from unittest.mock import Mock, patch

import pytest

from . import mockresponses

from citybikes.asyncio import Client
from citybikes.model import Network

@pytest.mark.asyncio
async def test_client(client):
    resp = await client.request(client.endpoint + 'v2/networks')
    assert resp

@pytest.mark.asyncio
async def test_default_ua():
    foo = Client()
    assert foo.session.headers['user-agent'] == Client.USER_AGENT

@pytest.mark.asyncio
async def test_given_ua():
    foo = Client(user_agent="hello world")
    assert foo.session.headers['user-agent'] == "hello world"

@pytest.mark.asyncio
async def test_arbitrary_session_args():
    mock = Mock()
    session_args = {"foo": 42, "bar": 33}
    with patch('aiohttp.ClientSession', mock):
        Client(user_agent="hello world", ** session_args)
        args, kwargs = mock.call_args
        assert session_args.items() <= kwargs.items()

@pytest.mark.asyncio
async def test_headers_preference():
    foo = Client(user_agent="hello world", headers={'user-agent': 'foo'})
    assert foo.session.headers['user-agent'] == "foo"

@pytest.mark.asyncio
async def test_networks(client):
    networks = await client.networks.fetch()
    assert networks == [Network.from_dict(n) for n in mockresponses.networks['networks']]

@pytest.mark.asyncio
async def test_network(client):
    network = await client.network(uid='foo').fetch()
    assert network == Network.from_dict(mockresponses.network['network'])


@pytest.mark.asyncio
async def test_networks_near(client):
    await client.networks.fetch()
    assert [n.id for n, dist in client.networks.near(0.0, 0.0)] == ['baz', 'bar', 'foo']
    assert [n.id for n, dist in client.networks.near(30.0, 1.0)] == ['bar', 'baz', 'foo']
    assert [n.id for n, dist in client.networks.near(100.0, 100.0)] == ['foo', 'bar', 'baz']

@pytest.mark.asyncio
async def test_stations_near(client):
    net = client.network(uid='foo')
    await net.fetch()
    assert [n.id for n, dist in net.near(0.0, 0.0)] == [1, 2, 3]
    assert [n.id for n, dist in net.near(25.0, 25.0)] == [2, 3, 1]
    assert [n.id for n, dist in net.near(100.0, 100.0)] == [3, 2, 1]
