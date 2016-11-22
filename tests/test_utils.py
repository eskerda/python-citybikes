# -*- coding: utf-8 -*-

from citybikes.utils import distance, dist_sort


class TestDistance:
    def test_distance_properties(self):
        battery = [
            # Identity
            ((1.1, 1.1), (1.1, 1.1), 0.0),
            # Abs
            ((1.0, 0.0), (-1.0, 0.0), 2.0),
        ]
        for xy, xy2, result in battery:
            assert distance(xy, xy2) == result

    def test_square(self):
        # c^2 + c^2 = hypot^2
        xy = (0.0, 0.0)
        xy2 = (2.5, 2.5)
        c = 2.5
        h = distance(xy, xy2)
        assert (c * c) * 2 == round(h * h, 2)


class TestDistanceSort:
    # List of points, already sorted by distance to 0.0
    points = [
        [0.0, 0.1],
        [0.1, 0.1],
        [0.2, 0.1],
        [0.2, 0.2],
        [8.0, 0.0],
        [5.0, 10.0],
        [11.0, 11.0],
    ]

    def test_eq(self):
        sorted_points = dist_sort([0.0, 0.0], self.points,
                                  lambda p: (p[0], p[1]))
        sorted_points = [latlng for latlng, dist in sorted_points]
        assert self.points == sorted_points

    def test_sort(self):
        sorted_points = dist_sort([10.0, 10.0], self.points,
                                  lambda p: (p[0], p[1]))
        sorted_points = [latlng for latlng, dist in sorted_points]
        assert list(reversed(self.points)) == sorted_points
