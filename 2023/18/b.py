from functools import cache, cached_property
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


@cache
def _direction(dir_str: str) -> Point2D:
    if dir_str == "3":
        return Point2D(0, 1)
    elif dir_str == "1":
        return Point2D(0, -1)
    elif dir_str == "2":
        return Point2D(-1, 0)
    elif dir_str == "0":
        return Point2D(1, 0)


def run(inputs: str) -> int:
    # https://en.wikipedia.org/wiki/Stokes%27_theorem

    area = 0
    location = Point2D(0, 0)
    perimiter = 0

    for line in inputs.splitlines():
        hex_value = line.split()[-1][1:-1]
        direction_str = hex_value[-1]
        steps = int(hex_value[1:-1], 16)
        direction = _direction(direction_str)

        location += steps * direction
        perimiter += steps

        if direction.y:
            new_area = location.x * steps
            if direction.y > 0:
                new_area *= -1
            area += new_area

    return area + perimiter // 2 + 1
