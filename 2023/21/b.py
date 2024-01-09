import numpy as np
import numba as nb


@profile
def step(
    locations: set[complex], rocks: set[complex], grid_height: int, grid_width: int
) -> set[complex]:
    new_locations = set()
    for location in locations:
        for direction in [complex(0, 1), complex(1, 0), complex(0, -1), complex(-1, 0)]:
            new_location = location + direction
            if new_location.real < 0 or new_location.real >= grid_width:
                continue
            if new_location.imag < 0 or new_location.imag >= grid_height:
                continue
            if new_location in rocks:
                continue
            new_locations.add(new_location)
    return new_locations


def run(inputs: str) -> int:
    rocks = set()
    grid_width, grid_height = None, 0
    starting_location = None

    for y, line in enumerate(inputs.splitlines()):
        characters = list(line)
        if not y:
            grid_width = len(characters)
        for x, c in enumerate(characters):
            if c == "#":
                rocks.add(complex(x, y))
            elif c == "S":
                starting_location = complex(x, y)
        grid_height += 1

    locations = set([starting_location])
    for _ in range(26501365):
        if _ % 10000 == 0:
            print(_, len(locations))
        locations = step(locations, rocks, grid_height, grid_width)

    return len(locations)
