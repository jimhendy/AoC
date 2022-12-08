import numpy as np
import numba


@numba.njit
def viewing_distance_from_top_to_bottom(grid):
    output = np.ones_like(grid)
    grid_height = grid.shape[0]
    for y, row in enumerate(grid):
        for x, tree_height in enumerate(row):
            if y == grid_height - 1:
                distance = 0
            else:
                for distance in range(1, grid_height - y):
                    if grid[y + distance, x] >= tree_height:
                        break
            output[y, x] = distance
    return output


def run(inputs):
    inputs = np.array(list(map(list, inputs.splitlines())), dtype=np.int8)

    return np.multiply.reduce(
        (
            viewing_distance_from_top_to_bottom(inputs),  # From top
            viewing_distance_from_top_to_bottom(inputs[::-1])[::-1],  # From bottom
            viewing_distance_from_top_to_bottom(inputs.T).T,  # From left
            viewing_distance_from_top_to_bottom(inputs.T[::-1])[::-1].T,  # From right
        )
    ).max()
