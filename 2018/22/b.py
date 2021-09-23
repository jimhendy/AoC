import os

from a_star import augemented_a_star as a_star
from cave import Cave, Terrain
from point import Point
from route import Equipment, Route


def run(inputs):
    inputs = inputs.split(os.linesep)
    depth = int(inputs[0].split(":")[1].strip())
    target = Point(
        int(inputs[1].split(":")[1].split(",")[0].strip()),
        int(inputs[1].split(":")[1].split(",")[1].strip()),
    )
    cave = Cave(depth, target)

    chosen_route = a_star(
        Route(Point(0, 0), cave, Equipment.Torch, 0),
        tag_func=lambda x: f"{x.pos} {x.equipment}",
    )

    grid = cave.__repr__()
    with open("mine.txt", "w") as f:
        for h in chosen_route.history:
            f.write(str(h))
            f.write("\n")

    return chosen_route.time
