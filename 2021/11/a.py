import os

import numpy as np

from tools.point import Point2D


def to_flash(oct, flashed):
    to_flash = []
    for x in range(oct.shape[1]):
        for y in range(oct.shape[0]):
            if oct[y, x] <= 9:
                continue
            p = Point2D(x, y)
            if p not in flashed:
                to_flash.append(p)
    return to_flash


def iterate(oct):
    flashed = set()
    oct += 1
    while points := to_flash(oct, flashed):
        for p in points:
            flashed.add(p)
            for n in p.nb8(grid_size=oct.shape):
                oct[n.y, n.x] += 1

    for p in flashed:
        oct[p.y, p.x] = 0

    return len(flashed)


def run(inputs):
    oct = np.array([list(i) for i in inputs.split(os.linesep)]).astype(int)
    return sum([iterate(oct) for _ in range(100)])
