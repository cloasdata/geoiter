import bisect

from typing import List, Tuple, Optional
from haversine import inverse_haversine, Direction, haversine

import math

Coordinate = Tuple[float, float]
Coordinates = List[Coordinate]

SQRT3BY2 = 0.8660254037844386


class GeoIter:
    def __init__(self,
                 boundary: Coordinates,
                 radius: float,
                 overlap: float = .05,
                 comp_rate: int = 0,
                 lat_offset: int = 0,
                 strict=False):
        """
        Implements the iter protocol.

        Here is how it works::

                        +---lat max-----+
            not strict x|   x   x   x   |
                        +   (offset)    +-----+ Start from here when offset ist provided
                        | x   x   x   x |     |
            not strict x|   x   x   x   |     V
                        | x   x   x   x |
                        +---lat min ----+

        :param boundary: A list of tuple(lat,lon floats)
        :param radius: The radius of each query in kilometres
        :param overlap: Overlap of circles by percentage. Default to 5%
        :param comp_rate: Compressions the boundary data by rate.
        :param lat_offset: Start the lat value with offset in kilometres
        :param strict: This forces the circles to be inside the boundary.
        """
        self.boundary = sorted(boundary)  # sort by lat
        self.radius = radius
        self.comp_rate = comp_rate
        if comp_rate:
            self._render_compression()

        self.lats, self.lons = zip(*self.boundary)
        self.distance = 2 * radius
        self.distance -= self.distance * overlap
        self.offset = lat_offset
        self.strict = strict

        self.delta = self.distance - self.distance * SQRT3BY2
        self._lat_max: Optional[Coordinate] = None
        self._lat_min: Optional[Coordinate] = None
        self._lat_distance: Optional[float] = None
        self._lon_max: Optional[Coordinate] = None
        self._lon_min: Optional[Coordinate] = None

        self._sort_lat: Optional[Coordinates] = None
        self._sort_lon: Optional[Coordinates] = None

        self._center: Optional[Coordinate] = None
        self._west_coordinates: Coordinates = []
        self._east_coordinates: Coordinates = []

        self._gen = None

    def _render_compression(self):
        reduce_to = len(self.boundary) / self.comp_rate
        ratio = round(len(self.boundary) / reduce_to, 1).as_integer_ratio()
        for _ in range(ratio[1]):
            self.boundary = self.boundary[::ratio[0]]

    def __iter__(self):
        return self

    def __next__(self) -> Coordinate:
        if not self._gen:
            self._gen = self._generator()
        try:
            return next(self._gen)
        except StopIteration:
            self._gen = self._generator()
            raise

    def _generator(self):
        # Building a high density grid within the provided geometry of nodes.
        #
        max_rows = int(self._round(haversine(self.lat_max, self.lat_min) / (SQRT3BY2 * self.distance), 0))
        # start height at center
        lat = self.lat_max[0], self.center[1]
        # calculate one of
        lat_plus = inverse_haversine(lat, self.radius, Direction.EAST)
        distance = self.radius
        for row in range(max_rows):
            if row % 2:
                # shorten the distance on each second row by sqrt(3) / 2
                distance = SQRT3BY2 * self.distance
                lat = self._south_from(lat, distance)[0], lat_plus[1]
            else:
                # reset the lon coordinate to the center one
                lat = lat[0], self.center[1]
                lat = self._south_from(lat, distance)

            border_west = self._intersect_lat_west(lat)
            border_east = self._intersect_lat_east(lat)
            distance_to_west_border = haversine(lat, border_west)
            distance_to_east_border = haversine(lat, border_east)
            if self.strict:
                steps_west = int(distance_to_west_border // self.distance)
                steps_east = int(distance_to_east_border // self.distance)
            else:
                steps_west = int(self._round(distance_to_west_border / self.distance))
                steps_east = int(self._round(distance_to_east_border / self.distance))

            coordinate = lat
            yield coordinate
            yield from self._go_from(coordinate, by_steps=steps_west, in_direction=Direction.WEST)
            yield from self._go_from(coordinate, by_steps=steps_east, in_direction=Direction.EAST)

    def _go_from(self, coordinate, by_steps, in_direction):
        for step in range(by_steps):
            coordinate = inverse_haversine(coordinate, self.distance, in_direction)
            yield coordinate

    @staticmethod
    def _round(number, ndigits=0):
        """Always round off
        https://stackoverflow.com/a/70285861
        """

        exp = number * 10 ** ndigits
        if abs(exp) - abs(math.floor(exp)) < 0.5:
            return type(number)(math.floor(exp) / 10 ** ndigits)
        return type(number)(math.ceil(exp) / 10 ** ndigits)

    @property
    def center(self) -> Coordinate:
        if not self._center:
            self._center = (
                (self.lat_max[0] + self.lat_min[0]) / 2,
                (self.lon_max[1] + self.lon_min[1]) / 2
            )
        return self._center

    @property
    def lat_max(self) -> Coordinate:
        lat_max = self.boundary[-1]
        if self.offset:
            lat_max = inverse_haversine(lat_max, self.offset, Direction.SOUTH)
        return lat_max

    @property
    def lat_min(self) -> Coordinate:
        return self.boundary[0]

    @property
    def lat_distance(self):
        if not self._lat_distance:
            self._lat_distance = haversine(self.lat_max, self.lat_min)
        return self._lat_distance

    @property
    def lon_max(self) -> Coordinate:
        return self.sort_lon[-1]

    @property
    def lon_min(self) -> Coordinate:
        return self.sort_lon[0]

    @property
    def sort_lon(self) -> Coordinates:
        if not self._sort_lon:
            self._sort_lon = sorted(self.boundary, key=lambda c: c[1])
        return self._sort_lon

    @staticmethod
    def _south_from(coordinate: Coordinate, by: float) -> Coordinate:
        """Return coordinate +distance in south direction"""
        return inverse_haversine(coordinate, by, Direction.SOUTH)

    @staticmethod
    def _east_from(coordinate: Coordinate, by: float) -> Coordinate:
        """Return coordinate + distance in east direction"""
        return inverse_haversine(coordinate, by, Direction.EAST)

    def _intersect_lat_west(self, coordinate: Coordinate) -> Coordinate:
        """Returns the most west coordinate lying west of median"""
        # old implementation 400ms. Now First lazy invoke 200 ms. next are < 1ms!
        # return min(self.west_of_median, key=lambda c: ((coordinate[0] - c[0]) ** 2))
        nearest_idx = bisect.bisect_left(self.lats, coordinate[0])
        west_idx = 0
        lon = self.center[1]
        while True:
            if self.lons[nearest_idx + west_idx] < lon:
                return self.boundary[nearest_idx + west_idx]
            elif self.lons[nearest_idx - west_idx] < lon:
                return self.boundary[nearest_idx - west_idx]
            else:
                west_idx += 1

    @property
    def _west_of_median(self):
        if not self._west_coordinates:
            self._west_coordinates = [coordinate for coordinate in self.boundary if coordinate[1] < self.center[1]]
        return self._west_coordinates

    def _intersect_lat_east(self, coordinate: Coordinate) -> Coordinate:
        # return min(self.east_of_median, key=lambda c: (coord[0] - c[0]) ** 2)
        nearest_idx = bisect.bisect_left(self.lats, coordinate[0])
        east_idx = 0
        lon = self.center[1]
        while True:
            if self.lons[nearest_idx + east_idx] > lon:
                return self.boundary[nearest_idx + east_idx]
            elif self.lons[nearest_idx - east_idx] > lon:
                return self.boundary[nearest_idx - east_idx]
            else:
                east_idx += 1

    @property
    def _east_of_median(self):
        if not self._east_coordinates:
            self._east_coordinates = [coordinate for coordinate in self.boundary if coordinate[1] > self.center[1]]
        return self._east_coordinates
