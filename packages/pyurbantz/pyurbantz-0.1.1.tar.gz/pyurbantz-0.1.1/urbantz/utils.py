from math import radians, cos, sin, asin, sqrt, trunc, floor, ceil

EARTH_RADIUS_KM = 6371


class Coordinates(object):
    """
    A helper class for GPS coordinates.
    """

    def __init__(self, lat=0, lng=0):
        """
        Get coordinates from decimal degrees.

        :param float lat: Latitude in decimal degrees.
        :param float lng: Longitude in decimal degrees.
        """
        self.lat = lat
        self.lng = lng

    def __repr__(self):
        return '{}(lat={}, lng={})'.format(
            self.__class__.__name__, self.lat, self.lng)

    def __str__(self):
        return ', '.join(tuple(self))

    def __hash__(self):
        return hash(tuple(self))

    def __len__(self):
        return 2

    def __length_hint__(self):
        return len(self)

    def __iter__(self):
        return (self.lat, self.lng)

    def __dict__(self):
        return {'lat': self.lat, 'lng': self.lng}

    def __eq__(self, other):
        return hasattr(other, 'lat') and hasattr(other, 'lng') and \
            tuple(self) == tuple(other)

    def __add__(self, other):
        if not hasattr(other, 'lat') or hasattr(other, 'lng'):
            return NotImplemented
        return self.__class__(
            lat=self.lat + other.lat,
            lng=self.lng + other.lng,
        )

    def __sub__(self, other):
        if not hasattr(other, 'lat') or hasattr(other, 'lng'):
            return NotImplemented
        return self.__class__(
            lat=self.lat - other.lat,
            lng=self.lng - other.lng,
        )

    def __pos__(self):
        return self

    def __neg__(self):
        return self.__class__(lat=-self.lat, lng=-self.lng)

    def __abs__(self):
        return self.__class__(lat=abs(self.lat), lng=abs(self.lng))

    def __round__(self, ndigits=None):
        return self.__class__(
            lat=round(self.lat, ndigits),
            lng=round(self.lng, ndigits),
        )

    def __trunc__(self):
        return self.__class__(lat=trunc(self.lat), lng=trunc(self.lng))

    def __floor__(self):
        return self.__class__(lat=floor(self.lat), lng=floor(self.lng))

    def __ceil__(self):
        return self.__class__(lat=ceil(self.lat), lng=ceil(self.lng))

    def to_radians(self):
        """
        Convert to a ``(lat, lng)`` tuple in radians.

        :returns: Coordinates in radians.
        :rtype: tuple(float, float)
        """
        return tuple(map(radians, self))

    def distance(self, other):
        """
        Compute Haversine distance between two coordinates in meters.

        :param other: Another pair of coordinates to compute distance against.
        :type other: Coordinates
        :returns: Distance between the two coordinates, in meters.
        :rtype: float
        """
        if not hasattr(other, 'to_radians'):
            raise NotImplementedError(
                'Distance requires a to_radians() method on both coordinates')
        lat1, lon1 = self.to_radians()
        lat2, lon2 = other.to_radians()
        dlon, dlat = lon2 - lon1, lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        return EARTH_RADIUS_KM * 2000 * asin(sqrt(a))

    def toJSON(self):
        """
        Convert to UrbanTZ JSON geometry

        :returns: UrbanTZ-compatible JSON geometry data
        :rtype: list(float)
        """
        return [self.lng, self.lat]

    @staticmethod
    def fromJSON(geometry):
        """
        Get a Coordinates instance from parsed UrbanTZ JSON geometry data.

        :param geometry: Parsed UrbanTZ geometry data: a list holding
           ``[lng, lat]`` in decimal degrees.
        :type geometry: list(float)
        """
        return Coordinates(lng=geometry[0], lat=geometry[1])
