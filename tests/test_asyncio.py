import pytest

from . import mockresponses

from citybikes.model import Network

@pytest.mark.asyncio
async def test_client(client):
    resp = await client.request(client.endpoint + 'v2/networks')
    assert resp

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
