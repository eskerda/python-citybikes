# -*- coding: utf-8 -*-
import re
import json

import responses

import citybikes
from . import mockresponses

"""
Pretty bare tests that check we can actually use this client as we intend
to for the API. Pretty bare and does not enter into testing how Resources
work :(
"""


class TestClient:
    def test_defaults(self):
        client = citybikes.Client()
        assert client.endpoint == client.DEFAULT_ENDPOINT
        client.networks

    def test_custom(self):
        client = citybikes.Client(
            endpoint='http://foobar.com',
            headers={"User-Agent": "Walrus 9000"},
        )
        assert client.endpoint == 'http://foobar.com'

    @responses.activate
    def test_default_user_agent(self):
        responses.add(responses.GET, 'http://example.com')
        client = citybikes.Client()
        resp = client.request('http://example.com', method='GET')
        assert client.USER_AGENT in resp.request.headers['User-Agent']

    @responses.activate
    def test_user_agent(self):
        responses.add(responses.GET, 'http://example.com')
        client = citybikes.Client(headers={"User-Agent": "foobar"})
        resp = client.request('http://example.com', method='GET')
        assert "foobar" in resp.request.headers['User-Agent']

    @responses.activate
    def test_requests_saved(self):
        responses.add(responses.GET, 'https://api.citybik.es/v2/networks',
                      json=mockresponses.networks)
        nets_url_re = re.compile(
            r'https:\/\/api\.citybik\.es\/v2\/networks\/.+'
        )
        responses.add(responses.GET, nets_url_re, json=mockresponses.network)
        client = citybikes.Client()
        list(client.networks)
        list(client.networks)
        assert len(responses.calls) == 1
        net = next(iter(client.networks))
        assert len(responses.calls) == 1
        list(net.stations)
        list(net.stations)
        list(net.stations)
        assert len(responses.calls) == 2


class TestNetworks:
    @responses.activate
    def test_networks(self):
        responses.add(responses.GET, 'https://api.citybik.es/v2/networks',
                      json=mockresponses.networks)
        client = citybikes.Client()
        networks = list(client.networks)
        assert len(networks) == 3
        assert client.networks.data == mockresponses.networks
        for n in networks:
            assert isinstance(n, citybikes.Network)

    @responses.activate
    def test_near_networks(self):
        responses.add(responses.GET, 'https://api.citybik.es/v2/networks',
                      json=mockresponses.networks)
        client = citybikes.Client()
        battery = [
            (client.networks.near(0.0, 0.0), ['baz', 'bar', 'foo']),
            (client.networks.near(30.0, 1.0), ['bar', 'baz', 'foo']),
            (client.networks.near(100.0, 100.0), ['foo', 'bar', 'baz']),
        ]
        for nets, expected in battery:
            assert [n['id'] for n, dist in nets] == expected

    @responses.activate
    def test_network_json(self):
        responses.add(responses.GET, 'https://api.citybik.es/v2/networks',
                      json=mockresponses.networks)
        client = citybikes.Client()
        assert json.dumps(client.networks, cls=citybikes.resource.JSONEncoder)


class TestNetwork:
    @responses.activate
    def test_network_by_uid(self):
        responses.add(responses.GET, 'https://api.citybik.es/v2/networks/foo',
                      json=mockresponses.network)
        client = citybikes.Client()
        foo = citybikes.Network(client, uid='foo')
        assert foo.data == mockresponses.network['network']

    @responses.activate
    def test_stations(self):
        responses.add(responses.GET, 'https://api.citybik.es/v2/networks/foo',
                      json=mockresponses.network)
        client = citybikes.Client()
        foo = citybikes.Network(client, uid='foo')
        stations = list(foo.stations)
        for s in stations:
            assert isinstance(s, citybikes.Station)

    @responses.activate
    def test_near_stations(self):
        responses.add(responses.GET, 'https://api.citybik.es/v2/networks/foo',
                      json=mockresponses.network)
        client = citybikes.Client()
        network = citybikes.Network(client, uid='foo')
        battery = [
            (network.stations.near(0.0, 0.0), [1, 2, 3]),
            (network.stations.near(25.0, 25.0), [2, 3, 1]),
            (network.stations.near(100.0, 100.0), [3, 2, 1]),
        ]
        for nets, expected in battery:
            assert [n['id'] for n, dist in nets] == expected

    @responses.activate
    def test_network_json(self):
        responses.add(responses.GET, 'https://api.citybik.es/v2/networks/foo',
                      json=mockresponses.network)
        client = citybikes.Client()
        network = citybikes.Network(client, uid='foo')
        assert json.dumps(network, cls=citybikes.resource.JSONEncoder)
