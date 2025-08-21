# -*- coding: utf-8 -*-

networks = {
    'networks': [
        {
            'href': '/v2/networks/foo',
            'id': 'foo',
            'location': {
                'city': 'Foo Land',
                'country': 'Fancyland',
                'latitude': 41.3850639,
                'longitude': 2.1734035,
            },
            'name': 'Foo Bike Share',
        },
        {
            'href': '/v2/networks/bar',
            'id': 'bar',
            'location': {
                'city': 'bar land',
                'country': 'fancybarland',
                'latitude': 31.3850639,
                'longitude': 1.1734035,
            },
            'name': 'bar bike share',
        },
        {
            'href': '/v2/networks/baz',
            'id': 'baz',
            'location': {
                'city': 'baz land',
                'country': 'fancybazland',
                'latitude': 21.3850639,
                'longitude': 0.1734035,
            },
            'name': 'baz bike share',
        },
    ]
}

network = {
    'network': {
        'href': '/v2/networks/foo',
        'id': 'foo',
        'location': {
            'city': 'Foo Land',
            'country': 'Fancyland',
            'latitude': 41.3850639,
            'longitude': 2.1734035,
        },
        'name': 'Foo Bike Share',
        'stations': [
            {
                "empty_slots": 25,
                "free_bikes": 13,
                "id": 1,
                "latitude": 10.401,
                "longitude": 2.1,
                "name": "Foo 1",
                "extra": {"some_field": 1,},
                "timestamp": "2025-08-21T14:00:23.164005+00:00Z",
            },
            {
                "empty_slots": 10,
                "free_bikes": 11,
                "id": 2,
                "latitude": 20.402,
                "longitude": 2.2,
                "name": "Foo 2",
                "extra": {"some_field": 2,},
                "timestamp": "2025-08-21T14:00:23.164005+00:00Z",
            },
            {
                "empty_slots": 3,
                "free_bikes": 5,
                "id": 3,
                "latitude": 30.403,
                "longitude": 2.3,
                "name": "Foo 3",
                "extra": {"some_field": 3,},
                "timestamp": "2025-08-21T14:00:23.164005+00:00Z",
            },
        ]
    }
}
