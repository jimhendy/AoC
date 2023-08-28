import os

from point import Point


def get_char(grid, point):
    return grid[point.y][point.x]


def set_char(grid, point, char):
    grid[point.y][point.x] = char


def update_grid(in_grid):
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
    return out_grid


def run(inputs):
    grid = [list(line) for line in inputs.split(os.linesep)]

    for _ in range(10):
        grid = update_grid(grid)

    single_str = "".join(["".join(row) for row in grid])
    return single_str.count("#") * single_str.count("|")
