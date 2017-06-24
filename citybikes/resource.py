# -*- coding: utf-8 -*-

import json
import asyncio
import aiohttp
from six.moves.urllib.parse import urljoin
from collections import MutableMapping


class Resource(MutableMapping):
    uri = None

    resource_class = None
    resource_path = None
    resource_wrap = None

    def __init__(self, client, data=None):
        self.client = client
        self.url = urljoin(client.endpoint, self.uri)
        self._data = data or {}

    @property
    def data(self):
        if not self.is_complete:
            self.request()
        return self._data

    @asyncio.coroutine
    @property
    def async_data(self):
        if not self.is_complete:
            yield from self.async_request()
        return self._data

    @property
    def is_complete(self):
        if not self._data:
            return False
        if self.resource_path and self.resource_path not in self._data:
            return False
        return True

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        things = self.get_resource()
        for x in things:
            yield self.resource_class(self.client, x)

    def __len__(self):
        return len(self.get_resource())

    def __delitem__(self, key):
        del self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def request(self, _path=None, **kwargs):
        if not self.client.loop:
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.async_request(_path, **kwargs))
            finally:
                loop.close()
        else:
            asyncio.run_coroutine_threadsafe(self.async_request(_path,
                **kwargs), self.client.loop).result()

    @asyncio.coroutine
    def async_request(self, _path=None, **kwargs):
        kwargs['method'] = 'GET'
        data = yield from self.client.async_request(
            urljoin(self.url, _path), **kwargs)
        if self.resource_wrap:
            data = data[self.resource_wrap]
        self._data.update(data)

    def get_resource(self):
        return self.get(self.resource_path)

    def __repr__(self):
        return repr(self.data)


class AbstractResource(Resource):
    def __init__(self, client, parent):
        super(AbstractResource, self).__init__(client, parent.data)
        self.parent = parent

    def request(self, *args, **kwargs):
        return self.parent.request(*args, **kwargs)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        return o.data
