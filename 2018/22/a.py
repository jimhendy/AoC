import os

from cave import Cave
from point import Point


def run(inputs):
    inputs = inputs.split(os.linesep)
    depth = int(inputs[0].split(":")[1].strip())
    target = Point(
        int(inputs[1].split(":")[1].split(",")[0].strip()),
        int(inputs[1].split(":")[1].split(",")[1].strip()),
    )
    cave = Cave(depth, target)

    total = 0
    for x in range(target.x + 1):
        for y in range(target.y + 1):
            total += cave.terrain(Point(x, y)).value

    return total
