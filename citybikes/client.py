# -*- coding: utf-8 -*-
import asyncio
import aiohttp

from citybikes import __version__ as _version
from citybikes.resource import AbstractResource, Resource
from citybikes.utils import dist_sort


class Client(object):

    DEFAULT_ENDPOINT = 'https://api.citybik.es/'
    USER_AGENT = 'python-citybikes/{version}'.format(version=_version)

    def __init__(self, endpoint=None, user_agent=None, loop=None):
        self.endpoint = endpoint or self.DEFAULT_ENDPOINT
        self.headers = {
            'User-Agent': user_agent or self.USER_AGENT
        }
        self.loop = loop
        self.networks = Networks(self)

    def request(self, url, **kwargs):
        return asyncio.wait(self.async_request(url, **kwargs))

    @asyncio.coroutine
    def async_request(self, url, **kwargs):
        kwargs['url'] = url
        session = aiohttp.ClientSession(loop=self.loop, headers=self.headers)
        response = yield from self.session.request(**kwargs)
        session.release()
        return response


class Network(Resource):
    uri = '/v2/networks/{uid}'
    resource_wrap = 'network'

    def __init__(self, client, data=None, uid=None):
        self.uri = data['href'] if data else self.uri.format(uid=uid)
        super(Network, self).__init__(client, data=data)
        self.stations = Stations(client, parent=self)


class Networks(Resource):
    uri = 'v2/networks'
    resource_class = Network
    resource_path = 'networks'

    def near(self, lat, lng):
        def getter(network):
            return (network['location']['latitude'],
                    network['location']['longitude'])
        return dist_sort([lat, lng], iter(self), getter)


class Station(Resource):
    pass


class Stations(AbstractResource):
    resource_class = Station
    resource_path = 'stations'

    def near(self, lat, lng):
        def getter(station):
            return (station['latitude'], station['longitude'])
        return dist_sort([lat, lng], iter(self), getter)
