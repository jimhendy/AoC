import os
from collections import defaultdict

from tools.point import PointyTop2DHexPoint as Point


def flip(black_tiles):
    bt_copy = black_tiles.copy()
    white_tiles = defaultdict(int)

    for bt in bt_copy:
        n_black_nb = 0
        for n in bt.all_neighbours():
            if n in bt_copy:
                n_black_nb += 1
            else:
                white_tiles[n] += 1
        if n_black_nb == 0 or n_black_nb > 2:
            black_tiles.remove(bt)

    for wt, n_black_nb in white_tiles.items():
        if n_black_nb == 2:
            black_tiles.add(wt)


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

    [flip(black_tiles) for _ in range(100)]

    return len(black_tiles)
