from urllib.parse import urljoin

import aiohttp

import citybikes.model as model
from citybikes.utils import dist_sort
from citybikes import __version__ as _version


class Resource:
    uri = None
    _data = None
    _repr = None

    def __init__(self, client, _data=None):
        self.client = client
        self._data = _data

    async def fetch(self, **kwargs):
        self._data = await self.client.request(url=self.url, **kwargs)
        self._repr = self.parse(self._data)
        return self._repr

    def parse(self, data):
        return data

    @property
    def url(self):
        return urljoin(self.client.endpoint, self.uri)

    def __getattr__(self, key):
        return getattr(self._repr, key)


class Networks(Resource):
    uri = '/v2/networks'

    def parse(self, data):
        return [model.Network.from_dict(n) for n in data['networks']]

    def near(self, lat, lng):
        def getter(network):
            return (network.location.latitude, network.location.longitude)
        return dist_sort([lat, lng], self._repr, getter)


class Network(Resource):
    uri = '/v2/networks/{uid}'

    def __init__(self, *args, uid, **kwargs):
        self.uid = uid
        super().__init__(*args, **kwargs)

    @property
    def url(self):
        return urljoin(self.client.endpoint, self.uri.format(uid=self.uid))

    def parse(self, data):
        return model.Network.from_dict(data['network'])

    def near(self, lat, lng):
        def getter(station):
            return (station.latitude, station.longitude)
        return dist_sort([lat, lng], self._repr.stations, getter)


class Client:
    DEFAULT_ENDPOINT = "https://api.citybik.es/"
    USER_AGENT = 'python-citybikes/{version}'.format(version=_version)


    _networks_list = None
    _networks = None

    def __init__(self, endpoint=None, headers=None):
        self.endpoint = endpoint or self.DEFAULT_ENDPOINT
        headers = headers or {}
        headers.setdefault("user-agent", self.USER_AGENT)
        self.session = aiohttp.ClientSession(headers=headers)
        self._networks = {}

    async def request(self, url, method="GET", **kwargs):
        async with self.session.request(method, url, **kwargs) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def close(self):
        await self.session.close()

    @property
    def networks(self):
        """ Singleton networks """
        if not self._networks_list:
            self._networks_list = Networks(self)
        return self._networks_list

    def network(self, uid):
        """ Singleton network """
        if uid not in self._networks:
            self._networks[uid] = Network(self, uid=uid)
        return self._networks[uid]
