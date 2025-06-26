from collections import namedtuple
from functools import cache, cached_property
from typing import Self

from matplotlib.path import Path


class Point2D(complex):
    @cached_property
    def x(self) -> int:
        return int(self.real)

    @cached_property
    def y(self) -> int:
        return int(self.imag)

    def __add__(self, other: Self) -> Self:
        return Point2D(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other: Self) -> Self:
        return Point2D(self.real - other.real, self.imag - other.imag)


@cache
def _direction(dir_str: str) -> Point2D:
    if dir_str == "3":
        return Point2D(0, 1)
    if dir_str == "1":
        return Point2D(0, -1)
    if dir_str == "2":
        return Point2D(-1, 0)
    if dir_str == "0":
        return Point2D(1, 0)


PerimiterLimits = namedtuple("PerimiterLimits", ["min_x", "max_x", "min_y", "max_y"])


@cache
def _perimiter_limits(perimiter: set[Point2D]) -> PerimiterLimits:
    min_x = min(p.x for p in perimiter)
    max_x = max(p.x for p in perimiter)
    min_y = min(p.y for p in perimiter)
    max_y = max(p.y for p in perimiter)
    return PerimiterLimits(min_x, max_x, min_y, max_y)


def _find_starting_location(perimiter_path: Path, perimiter: set[Point2D]) -> Point2D:
    """Locate a cell within the perimiter.

    We start from complex(0, 0) and find a cell near it within the shape
    of the perimiter.
    """
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            location = Point2D(dx, dy)
            if location in perimiter:
                continue
            if perimiter_path.contains_point([location.x, location.y]):
                return location


def _flood_fill(perimiter: set[Point2D], starting_location: Point2D) -> set[Point2D]:
    internal_points = {starting_location}
    queue = [starting_location]
    while queue:
        location = queue.pop()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0:
                    continue
                new_location = location + Point2D(dx, dy)
                if new_location in perimiter:
                    continue
                if new_location in internal_points:
                    continue
                internal_points.add(new_location)
                queue.append(new_location)
    return internal_points


def run(inputs: str) -> int:
    location = Point2D(0, 0)
    perimiter_intersections = [location]
    for line in inputs.splitlines():
        hex_value = line.split()[-1][1:-1]
        direction_str = hex_value[-1]
        steps = int(hex_value[1:-1], 16)
        direction = _direction(direction_str)
        location += steps * direction
        perimiter_intersections.append(location)

    perimiter_path = Path([[p.x, p.y] for p in perimiter_intersections])

    perimiter = frozenset(perimiter_intersections)

    starting_location = _find_starting_location(perimiter_path, perimiter)

    print(starting_location)

    return len(perimiter)
