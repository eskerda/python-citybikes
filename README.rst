python-citybikes
================
`python-citybikes` is a python client for the `Citybikes API`_.

About Citybikes
---------------
Citybikes_ is a project about making bike sharing data available to both users
and developers. It has a nice and easy to use API, but this package might be
useful to projects consuming the API.

``python-citybikes`` must not be confused with `pybikes`_:

- `pybikes`_ is a set of tools to access bike sharing data directly from the providers. It's the library powering the project and the API. If a network is not supported or does not correctly work, it's there where the issue or the contribution must be sent.
- `python-citybikes` is a python wrapper around the `Citybikes API`_.

.. _Citybikes: https://citybik.es
.. _Citybikes API: https://api.citybik.es
.. _pybikes: https://github.com/eskerda/pybikes


Installation
------------

.. code-block::

    $ pip install python-citybikes

Usage
-----
First instantiate a client

.. code-block::

    >>>> import citybikes
    >>>> client = citybikes.Client()

Get the full list of networks

.. code-block::

    >>>> networks = list(client.networks)
    >>>> len(networks)
    458
    >>>> networks[0]
    {'name': 'Opole Bike', 'href': '/v2/networks/opole-bike', 'location': {'lat
    itude': 50.6645, 'city': 'Opole', 'country': 'PL', 'longitude': 17.9276}, '
    id': 'opole-bike', 'company': ['Nextbike GmbH']}

Get stations from a network

.. code-block::

    >>>> len(networks[0].stations)
    16
    >>>> list(networks[0].stations)[0]
    {'timestamp': '2016-11-22T16:05:44.318000Z', 'id': 'd8c9f66260759aeb27445b2
    cddf2d6b9', 'name': 'Pętla Autobusowa - Dambonia', 'free_bikes': 7, 'empty_
    slots': 3, 'latitude': 50.661775266224, 'extra': {'bike_uids': ['60128', '6
    0108', '60063', '60062', '60052', '60037', '60190'], 'number': '6011', 'slo
    ts': 10, 'uid': '132115'}, 'longitude': 17.888891100884}

Instantiate a network by id directly

.. code-block::

    >>>> bicing = citybikes.Network(client, uid='bicing')
    >>>> bicing['name']
    'Bicing'
    >>>> len(bicing.stations)
    465

Get a network ordered by distance to lat, lng

.. code-block::

    >>>> # Lets get the nearest network to NY lat, lng
    >>>> net, dist = next(iter(client.networks.near(40.7128, -74.0059)))
    >>>> net
    {'href': '/v2/networks/citi-bike-nyc', 'id': 'citi-bike-nyc', 'gbfs_href': 
    'https://gbfs.citibikenyc.com/gbfs/gbfs.json', 'location': {'latitude': 40.
    7143528, 'country': 'US', 'longitude': -74.00597309999999, 'city': 'New Yor
    k, NY'}, 'company': ['NYC Bike Share, LLC', 'Motivate International, Inc.',
    'PBSC Urban Solutions'], 'name': 'Citi Bike'}

Get stations from a network ordered by distance to lat, lng

.. code-block::

    >>>> # Now, get stations ordered by distance to Manhattan center
    >>>> sts = net.stations.near(40.7831, -73.9712)
    >>>> for s, dist in sts[:5]:
    ...     print(s['name'])
    ...
    W 82 St & Central Park West
    Central Park West & W 85 St
    W 84 St & Columbus Ave
    Central Park West & W 76 St
    W 89 St & Columbus Ave

