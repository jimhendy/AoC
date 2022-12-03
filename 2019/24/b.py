import os

import numba
import numpy as np

BUG = ord("#")
EMPTY = ord(".")
MIDDLE = ord("?")


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


@numba.njit(numba.int8(numba.int8[:, :], numba.int8, numba.int8, numba.int8))
def update_cell(grid, x, y, extra):
    char = grid[y][x]
    if char == MIDDLE:
        return MIDDLE
    n_bugs = get_num_bugs(grid, x, y) + extra
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


@numba.njit(numba.int8(numba.int8[:]))
def count_bugs(inputs):
    return np.count_nonzero(inputs == BUG)


# @numba.njit(numba.int8[:,:](numba.int8[:,:], numba.int8[:,:], numba.int8[:,:]))
def update(grid_orig, grid_up, grid_down):
    grid = grid_orig.copy()
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):

            extra = 0

            if x == 0:
                # right edge up
                extra = count_bugs(grid_up[2][1:2])
            elif x == 4:
                # left edge up
                extra = count_bugs(grid_up[2][3:4])
            elif x == 1 and y == 2:
                # left edge down
                extra = count_bugs(grid_down[:, 0])
            elif x == 3 and y == 2:
                # right edge down
                extra = count_bugs(grid_down[:, 4])
            elif y == 1 and x == 2:
                # top edge down
                extra = count_bugs(grid_down[0])
            elif y == 3 and x == 2:
                # bottom edge down
                extra = count_bugs(grid_down[4])
                pass

            # top/bottom
            if y == 0:
                # bottom edge up
                extra += count_bugs(grid_up[1][2:3])
            elif y == 4:
                extra += count_bugs(grid_up[3][2:3])
                pass

            grid[y][x] = update_cell(grid_orig, x, y, extra)
            pass
        pass
    return grid


# @numba.njit(numba.int8[:,:])
def new_grid():
    n = np.full((5, 5), EMPTY, dtype=np.int8)
    n[2][2] = MIDDLE
    return n


def run(inputs):

    grids = {
        0: np.array(
            [np.array(list(map(ord, i))) for i in inputs.split(os.linesep)]
        ).astype(np.int8)
    }
    grids[0][2][2] = MIDDLE
    grids[-1] = new_grid()
    grids[1] = new_grid()

    for _ in range(200):

        levels = list(grids.keys())
        new_grids = {}

        for level in levels:

            grid = grids[level]

            # if not len(np.argwhere( grid == BUG )):
            #    continue

            up = level - 1
            down = level + 1

            if not up in grids:
                grids[up] = new_grid()
                new_grids[up] = new_grid()
            if not down in grids:
                grids[down] = new_grid()
                new_grids[down] = new_grid()
                pass

            new_grids[level] = update(grid, grids[up], grids[down])

            pass

        grids = new_grids

        keys = sorted(list(grids.keys()))
        for k in keys:
            v = grids[k]

            current = np.count_nonzero(grids[k] == BUG)
            if current:
                continue

            if k - 1 in grids.keys():
                down = np.count_nonzero(grids[k - 1] == BUG)
            else:
                down = 0

            if down:
                continue

            if k + 1 in grids.keys():
                up = np.count_nonzero(grids[k + 1] == BUG)
            else:
                up = 0

            if up:
                continue

            del grids[k]

        pass

    result = sum([np.count_nonzero(g == BUG) for g in grids.values()])

    return result
