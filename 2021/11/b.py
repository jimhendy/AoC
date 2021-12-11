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

            for n in p.nb8():

                if n.x[0] < 0 or n.x[0] >= oct.shape[1]:
                    continue
                if n.x[1] < 0 or n.x[1] >= oct.shape[0]:
                    continue

                oct[n.x[1], n.x[0]] += 1

    for p in flashed:
        oct[p.x[1], p.x[0]] = 0

    return len(flashed)


def run(inputs):
    oct = np.array([list(i) for i in inputs.split(os.linesep)]).astype(int)

    steps = 0
    while True:
        flashes = iterate(oct)
        if flashes == oct.shape[0] * oct.shape[1]:
            return steps + 1
        steps += 1
