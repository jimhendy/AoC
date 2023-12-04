import os

from point import NEIGHBOUR_DELTAS, Point


def get_char(p, grid):
    return grid[p.y][p.x]


def set_char(p, grid, char):
    grid[p.y][p.x] = char


def seat_outside_range(p, grid):
    if p.x < 0 or p.y < 0:
        return True
    if p.x >= len(grid[0]) or p.y >= len(grid):
        return True
    return False


def find_neighbour_char(p, d, grid):
    while True:
        p = p.neighbour(d)
        if seat_outside_range(p, grid):
            return None
        char = get_char(p, grid)
        if char == ".":
            continue
        return char


def update_seats(in_grid):
    out_grid = [row[:] for row in in_grid]
    for row_num, row in enumerate(in_grid):
        for col_num, char in enumerate(row):
            if char == ".":
                continue

            p = Point(x=col_num, y=row_num)
            is_empty = char == "L"
            n_occupied = 0

            for d in NEIGHBOUR_DELTAS:
                char = find_neighbour_char(p, d, in_grid)
                n_occupied += char == "#"

            if is_empty and not n_occupied:
                set_char(p, out_grid, "#")
            elif not is_empty and n_occupied >= 5:
                set_char(p, out_grid, "L")

    return out_grid


def grid_str(grid):
    return os.linesep.join(["".join(row) for row in grid])


def run(inputs):
    grid = [list(line) for line in inputs.split(os.linesep)]
    seen = {grid_str(grid)}
    iteration = 0
    while True:
        print(f"Iteration: {iteration}")
        grid = update_seats(grid)
        s = grid_str(grid)
        if s in seen:
            break
        seen.add(s)
        iteration += 1

    return grid_str(grid).count("#")
