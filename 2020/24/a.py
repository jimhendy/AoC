import os

from tools.point import PointyTop2DHexPoint as Point

def run(inputs):
    black_tiles = set()

    for line in inputs.split(os.linesep):
        pos = Point(0, 0)
        line = list(line)
        while len(line):
            d = line.pop(0)
            if d in ("n", "s"):
                d += line.pop(0)
            pos += pos.steps[d]
        if pos in black_tiles:
            black_tiles.remove(pos)
        else:
            black_tiles.add(pos)

    return len(black_tiles)
