"""Define various utility functions."""
from math import radians, cos, sin, asin, sqrt


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Determine the distance between two latitude/longitude pairs."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    calc_a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    calc_c = 2 * asin(sqrt(calc_a))

    return 6371 * calc_c
