import os
from collections import defaultdict

import pandas as pd


def right(direction):
    return {(-1, 0): (0, +1), (0, +1): (+1, 0), (+1, 0): (0, -1), (0, -1): (-1, 0)}[
        direction
    ]


def left(direction):
    return {(-1, 0): (0, -1), (0, +1): (-1, 0), (+1, 0): (0, +1), (0, -1): (+1, 0)}[
        direction
    ]


def burst(grid, current_node, direction):
    infected = grid[current_node]
    turn = right if infected else left
    direction = turn(direction)
    grid[current_node] = not infected
    new_node = (current_node[0] + direction[0], current_node[1] + direction[1])
    return direction, new_node, not infected


def print_grid(grid, current_node, burst_num):
    print("-" * 30)
    print(burst_num)
    if current_node not in grid:
        grid[current_node] = False
    df = (
        pd.DataFrame(
            [
                {"row": k[0], "col": k[1], "value": "#" if v else "."}
                for k, v in grid.items()
            ],
        )
        .pivot_table(index="row", columns="col", values="value", aggfunc="first")
        .fillna(".")
    )
    df.loc[current_node[0], current_node[1]] = (
        "[" + df.loc[current_node[0], current_node[1]] + "]"
    )
    print(df)
    print("-" * 30)
    pass


def run(inputs):
    grid = defaultdict(lambda: False)
    for row_num, row in enumerate(inputs.split(os.linesep)):
        for col_num, char in enumerate(row):
            if char == "#":
                grid[(row_num, col_num)] = True

    current_pos = ((row_num + 1) // 2, (col_num + 1) // 2)
    direction = (-1, 0)
    n_infected = 0
    n_bursts = 10_000

    for _burst_num in range(1, n_bursts + 1):
        direction, current_pos, new_infection = burst(grid, current_pos, direction)
        n_infected += new_infection

    return n_infected
