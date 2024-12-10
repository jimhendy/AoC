import numpy as np


def routes(starting_location: np.ndarray, grid: np.ndarray) -> int:
    total = 0
    queue = [starting_location]
    while queue:
        location = queue.pop(0)
        current = grid[location[0], location[1]]
        if current == 9:
            total += 1
            continue
        for step in (
            np.array([0, 1]),
            np.array([0, -1]),
            np.array([1, 0]),
            np.array([-1, 0]),
        ):
            new_location = location + step
            if (
                not 0 <= new_location[0] < grid.shape[0]
                or not 0 <= new_location[1] < grid.shape[1]
            ):
                continue
            try:
                if grid[new_location[0], new_location[1]] == current + 1:
                    queue.append(new_location)
            except IndexError:
                pass

    return total


def run(inputs: str) -> int:
    grid = np.array([list(line) for line in inputs.splitlines()]).astype(int)

    starting_locations = np.argwhere(grid == 0)
    total = sum(
        routes(starting_location, grid) for starting_location in starting_locations
    )
    return total
