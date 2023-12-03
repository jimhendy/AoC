from tools.point import Point2D
import re
from dataclasses import dataclass
from typing import Iterable

NUMERIC_REG = re.compile(r"(\d+)")


@dataclass
class Gear:
    location: Point2D
    part_numbers: list[int]

    def ratio(self) -> int:
        if len(self.part_numbers) != 2:
            return 0
        return self.part_numbers[0] * self.part_numbers[1]


def _is_gear(c: str) -> bool:
    return c == "*"


def _adjacent_gear_locations(
    number: re.Match, grid: list[str], y: int, grid_size: tuple[int, int]
) -> Iterable[Point2D]:
    considered = set()
    for x in range(number.start(), number.end()):
        point = Point2D(x, y)
        for neighbour in point.nb8(grid_size=grid_size):
            if neighbour in considered:
                continue
            considered.add(neighbour)
            if _is_gear(grid[neighbour.y][neighbour.x]):
                yield neighbour


def run(inputs: str) -> int:
    grid = inputs.splitlines()
    grid_size = (len(grid[0]), len(grid))

    gears: dict[Point2D, Gear] = {}

    for y, line in enumerate(grid):
        for number in NUMERIC_REG.finditer(line):
            for gear_location in _adjacent_gear_locations(number, grid, y, grid_size):
                part_number = int(number.group(0))
                if not gear_location in gears:
                    gears[gear_location] = Gear(gear_location, [part_number])
                else:
                    gears[gear_location].part_numbers.append(part_number)

    return sum(gear.ratio() for gear in gears.values())
