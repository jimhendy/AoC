import os

from point import Point
from tqdm import tqdm

CACHE = {}


def get_char(grid, point):
    return grid[point.y][point.x]


def set_char(grid, point, char):
    grid[point.y][point.x] = char


def update_grid(in_grid, i):
    key = get_single_str(in_grid)
    out_grid = [l[:] for l in in_grid]
    for row_num, row in enumerate(in_grid):
        for col_num in range(len(row)):

            p = Point(x=col_num, y=row_num)

            n_yards = 0
            n_trees = 0

            c = get_char(in_grid, p)
            is_open = c == "."
            is_trees = c == "|"
            is_yard = c == "#"

            for n in p.nb8():
                if n.x < 0 or n.y < 0 or n.x >= len(row) or n.y >= len(in_grid):
                    continue
                c = get_char(in_grid, n)
                if c == "|":
                    n_trees += 1
                elif c == "#":
                    n_yards += 1

            if is_open and n_trees >= 3:
                set_char(out_grid, p, "|")
            elif is_trees and n_yards >= 3:
                set_char(out_grid, p, "#")
            elif is_yard:
                if n_yards and n_trees:
                    pass
                else:
                    set_char(out_grid, p, ".")
    previous_i = CACHE.get(key)
    CACHE[key] = i
    return out_grid, previous_i


def get_single_str(grid):
    return "".join(["".join(row) for row in grid])


def run(inputs):
    grid = [list(line) for line in inputs.split(os.linesep)]

    total_i = int(1e9)
    for i in tqdm(range(total_i)):
        grid, previous_i = update_grid(grid, i)
        if isinstance(previous_i, int):
            print(previous_i)
            break

    period = i - previous_i
    remaining_i = (total_i - i) % period - 1

    for i in tqdm(range(remaining_i)):
        grid, _ = update_grid(grid, i)

    single_str = get_single_str(grid)
    return single_str.count("#") * single_str.count("|")
