import os
import pandas as pd
from collections import defaultdict

CLEAN = "."
INFECTED = "#"
WEAKENED = "W"
FLAGGED = "F"


def right(direction):
    return {(-1, 0): (0, +1), (0, +1): (+1, 0), (+1, 0): (0, -1), (0, -1): (-1, 0)}[
        direction
    ]


def left(direction):
    return {(-1, 0): (0, -1), (0, +1): (-1, 0), (+1, 0): (0, +1), (0, -1): (+1, 0)}[
        direction
    ]


def reverse(direction):
    return (-1 * direction[0], -1 * direction[1])


def turn(node_state):
    return {CLEAN: left, WEAKENED: lambda x: x, INFECTED: right, FLAGGED: reverse,}[
        node_state
    ]


def new_state(current_state):
    return {CLEAN: WEAKENED, WEAKENED: INFECTED, INFECTED: FLAGGED, FLAGGED: CLEAN,}[
        current_state
    ]


def burst(grid, current_node, direction):
    current_state = grid[current_node]
    direction = turn(current_state)(direction)
    state = new_state(current_state)
    grid[current_node] = state
    new_node = (current_node[0] + direction[0], current_node[1] + direction[1])
    return direction, new_node, state == INFECTED


def print_grid(grid, current_node, burst_num):
    print("-" * 30)
    print(burst_num)
    if not current_node in grid.keys():
        grid[current_node] = CLEAN
    df = (
        pd.DataFrame([{"row": k[0], "col": k[1], "value": v} for k, v in grid.items()])
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
    grid = defaultdict(lambda: CLEAN)
    for row_num, row in enumerate(inputs.split(os.linesep)):
        for col_num, char in enumerate(row):
            grid[(row_num, col_num)] = char

    current_pos = ((row_num + 1) // 2, (col_num + 1) // 2)
    direction = (-1, 0)
    n_infected = 0
    n_bursts = 10000000
    debug = False

    if debug:
        print_grid(grid, current_pos, 0)
    for burst_num in range(1, n_bursts + 1):
        direction, current_pos, new_infection = burst(grid, current_pos, direction)
        n_infected += new_infection
        if debug:
            print_grid(grid, current_pos, burst_num)

    return n_infected
