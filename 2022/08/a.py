import numpy as np


def visible_from_top(grid):
    top_view = np.roll(np.maximum.accumulate(grid, axis=0), shift=1, axis=0)
    top_view[0] = -1
    return np.greater(grid, top_view)


def run(inputs):
    inputs = np.array(list(map(list, inputs.splitlines())), dtype=np.int8)

    return np.logical_or.reduce(
        (
            visible_from_top(inputs),  # From top
            visible_from_top(inputs[::-1])[::-1],  # From bottom
            visible_from_top(inputs.T).T,  # From left
            visible_from_top(inputs.T[::-1])[::-1].T,  # From right
        )
    ).sum()
