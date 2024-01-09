from functools import cached_property
from typing import Self


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


def step(
    locations: set[Point2D], rocks: set[Point2D], grid_height: int, grid_width: int
) -> set[Point2D]:
    new_locations = set()
    for location in locations:
        for direction in [Point2D(0, 1), Point2D(1, 0), Point2D(0, -1), Point2D(-1, 0)]:
            new_location = location + direction
            if new_location.x < 0 or new_location.x >= grid_width:
                continue
            if new_location.y < 0 or new_location.y >= grid_height:
                continue
            if new_location in rocks:
                continue
            new_locations.add(new_location)
    return new_locations


def run(inputs: str) -> int:
    rocks = set()
    grid_width, grid_height = None, 0
    starting_location = None

    for y, line in enumerate(inputs.splitlines()):
        characters = list(line)
        if not y:
            grid_width = len(characters)
        for x, c in enumerate(characters):
            if c == "#":
                rocks.add(Point2D(x, y))
            elif c == "S":
                starting_location = Point2D(x, y)
        grid_height += 1

    locations = set([starting_location])
    for _ in range(64):
        locations = step(locations, rocks, grid_height, grid_width)

    return len(locations)
