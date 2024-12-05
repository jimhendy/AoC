from collections import deque

from tools.inputs import parse_grid, nb4
from typing import Callable


def run(inputs: str) -> int:
    grid_size = len(inputs.splitlines())
    grid = parse_grid(inputs, ignore_chars="#")
    plot_locations = set(grid)

    visited: dict[complex, int] = {}
    queue: deque[tuple[int, complex]] = deque(
        [(0, next(k for k, v in grid.items() if v == "S"))]
    )

    while queue:
        distance, point = queue.popleft()

        if point in visited:
            continue

        visited[point] = distance

        for n in nb4(point):
            if n in visited or n not in plot_locations:
                continue

            queue.append((distance + 1, n))

    def num_points_where(f: Callable[[int], bool]) -> int:
        return sum(f(v) for v in visited.values())

    distance_to_edge = grid_size // 2
    assert distance_to_edge == 65  # checking assumptions is good!

    # hardcoding for the puzzle input
    n = (26501365 - distance_to_edge) // grid_size
    assert n == 202300, f"n calc wrong, got {n}"
    num_odd_tiles = (n + 1) ** 2
    num_even_tiles = n**2

    odd_corners = num_points_where(lambda v: v > distance_to_edge and v % 2 == 1)
    even_corners = num_points_where(lambda v: v > distance_to_edge and v % 2 == 0)

    part_2 = (
        num_odd_tiles * num_points_where(lambda v: v % 2 == 1)
        + num_even_tiles * num_points_where(lambda v: v % 2 == 0)
        - ((n + 1) * odd_corners)
        + (n * even_corners)
    )

    return part_2
