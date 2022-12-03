import heapq

import numpy as np
from knot_hash import knot_hash


def kh_to_binary(kh):
    return "".join(map(lambda x: bin(int(x, 16))[2:].zfill(4), kh))


def fill_region(grid, row_num, col_num):
    assert grid[row_num][col_num] == 1
    q = [(row_num, col_num)]
    while len(q):
        loc = heapq.heappop(q)
        if grid[loc[0]][loc[1]] != 1:
            continue
        grid[loc[0]][loc[1]] = 2
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr and dc:
                    continue
                r = loc[0] + dr
                c = loc[1] + dc
                if r < 0 or c < 0:
                    continue
                if r >= grid.shape[0] or c >= grid.shape[1]:
                    continue
                heapq.heappush(q, (r, c))
    return grid


def count_regions(grid):
    n_regions = 0
    g = grid.copy()
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if g[r][c] != 1:
                continue
            n_regions += 1
            g = fill_region(grid, r, c)
    return n_regions


def run(inputs):
    grid = np.zeros((128, 128))
    for i in range(128):
        kh = knot_hash(f"{inputs}-{i}")
        bin_rep = kh_to_binary(kh)
        grid[i] = list(map(int, bin_rep))
    n_regions = count_regions(grid)
    return n_regions
