from collections import deque
from typing import TYPE_CHECKING

from tools.point import Point3D as Point

if TYPE_CHECKING:
    from collections.abc import Iterable


def run(inputs):
    drops = {Point(*map(int, l.split(","))) for l in inputs.splitlines()}

    mins = [min(d.values[i] - 2 for d in drops) for i in range(3)]
    maxs = [max(d.values[i] + 2 for d in drops) for i in range(3)]
    starting_point = Point(*mins)

    total_faces = 0
    free_spaces: Iterable[Point] = deque([starting_point])
    seen = set()

    while free_spaces:
        p = free_spaces.pop()
        if p in seen:
            continue
        seen.add(p)

        for n in p.all_neighbours():
            if n in seen:
                continue
            if any(not mins[i] <= n.values[i] <= maxs[i] for i in range(3)):
                continue
            if n in drops:
                total_faces += 1
            else:
                free_spaces.append(n)

    return total_faces
