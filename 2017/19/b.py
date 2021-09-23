import os

import a_star
import maze


def run(inputs):
    grid = [list(row) for row in inputs.split(os.linesep)]
    start_row = 0
    start_col = [col for col, char in enumerate(grid[start_row]) if char == "|"][0]
    initial_state = maze.Maze(grid, start_row, start_col)

    solution = a_star.augmented_a_star(initial_state)

    return solution.n_steps + 1
