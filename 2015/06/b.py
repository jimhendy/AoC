import os
import re

import numba
import numpy as np


@numba.njit
def turn_on(current):
    return current + 1


@numba.njit
def turn_off(current):
    return max([current - 1, 0])


@numba.njit
def toggle(current):
    return current + 2


@numba.njit
def update(lights, start, end, func):
    for x in range(start[0], end[0] + 1):
        for y in range(start[1], end[1] + 1):
            lights[x][y] = func(lights[x][y])


def run(inputs):
    lights = np.full((1000, 1000), 0)
    reg = re.compile(r"(.+) (\d+)\,(\d+) through (\d+)\,(\d+)")

    funcs = {"turn on": turn_on, "turn off": turn_off, "toggle": toggle}

    for line in inputs.split(os.linesep):
        groups = reg.findall(line)[0]
        start = (int(groups[1]), int(groups[2]))
        end = (int(groups[3]), int(groups[4]))
        func = funcs[groups[0]]

        update(lights, start, end, func)

    return np.sum(lights)
