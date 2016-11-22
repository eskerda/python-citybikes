from math import hypot


def distance(xy, xy2):
    """ Gets euclidian distance between two pairs of points (x, y)
    :param xy: pair (x, y)
    :param xy2: pair (x, y)
    :return: float

    """
    return hypot(xy[0] - xy2[0], xy[1] - xy2[1])


def dist_sort(xy, locations, getter):
    """ Sorts a list of objects by distance to x, y
    :param xy: pair (x, y)
    :param locations: list of things to sort
    :param getter: function(location) must return pair (x, y)
    :return: list of locations sorted by distance to x, y

    """
    return sorted(
        map(lambda loc: [loc, distance(xy, getter(loc))], locations),
        key=lambda locdst: locdst[1]
    )
