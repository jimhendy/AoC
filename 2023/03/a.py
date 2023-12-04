import re

from tools.point import Point2D

NUMERIC_REG = re.compile(r"(\d+)")


def _is_symbol(c: str) -> bool:
    return not c.isnumeric() and c != "."

def _part_number(
    number: re.Match,
    grid: list[str],
    y: int,
    grid_size: tuple[int, int],
) -> int:
    for x in range(number.start(), number.end()):
        point = Point2D(x, y)
        for neighbour in point.nb8(grid_size=grid_size):
            if _is_symbol(grid[neighbour.y][neighbour.x]):
                return int(number.group(0))
    return 0

def run(inputs: str) -> int:
    grid = inputs.splitlines()
    grid_size = (len(grid[0]), len(grid))

    total = 0

    for y, line in enumerate(grid):
        for number in NUMERIC_REG.finditer(line):
            total += _part_number(number, grid, y, grid_size)

    return total
