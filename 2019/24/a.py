import os

import numba
import numpy as np

BUG = 35
EMPTY = 46


@numba.njit(numba.int8(numba.int8[:, :], numba.int8, numba.int8))
def get_num_bugs(grid, x, y):
    num_bugs = 0
    if x != 0 and grid[y][x - 1] == BUG:
        num_bugs += 1
        pass
    if x != (grid.shape[1] - 1) and grid[y][x + 1] == BUG:
        num_bugs += 1
        pass
    if y != 0 and grid[y - 1][x] == BUG:
        num_bugs += 1
        pass
    if y != (grid.shape[0] - 1) and grid[y + 1][x] == BUG:
        num_bugs += 1
        pass
    return num_bugs


@numba.njit(numba.int8(numba.int8[:, :], numba.int8, numba.int8))
def update_cell(grid, x, y):
    char = grid[y][x]
    n_bugs = get_num_bugs(grid, x, y)
    if char == BUG:
        if n_bugs == 1:
            return BUG
        else:
            return EMPTY
        pass
    else:
        if n_bugs == 1 or n_bugs == 2:
            return BUG
        else:
            return EMPTY
        pass
    pass


def plot(grid):
    for row in grid:
        for char in row:
            print(chr(char), end="")
            pass
        print()
        pass
    print()
    pass


@numba.njit(numba.int8[:, :](numba.int8[:, :]))
def update(grid_orig):
    grid = grid_orig.copy()
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            grid[y][x] = update_cell(grid_orig, x, y)
            pass
        pass
    return grid


def run(inputs):

    grid = np.array(
        [np.array(list(map(ord, i))) for i in inputs.split(os.linesep)]
    ).astype(np.int8)
    hashes = set()

    while True:
        grid = update(grid)
        h = hash(grid.tostring())
        if h in hashes:
            break
        hashes.add(h)
        pass

    result = 0
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == BUG:
                p = y * grid.shape[1] + x
                result += 2**p

    return result
