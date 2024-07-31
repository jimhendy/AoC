from loguru import logger
import numba as nb
import numpy as np

REPEATS = 5_000
OFFSET = REPEATS * 2


@nb.njit
def _x(num: int) -> int:
    return num // OFFSET


@nb.njit
def _y(num: int) -> int:
    return num % OFFSET


@nb.njit
def _num(x, y) -> int:
    return x * OFFSET + y


@nb.njit
def orig_location(loc: int, grid_height: int, grid_width: int) -> int:
    x = _x(loc)
    y = _y(loc)
    return _num(x % grid_width, y % grid_height)


@nb.njit
def all_steps(
    starting_location: int, rocks: np.ndarray[int], grid_width: int, grid_height: int
) -> int:
    locations = set([starting_location])
    rocks = set(rocks)

    for _ in range(REPEATS):  # 26501365):
        if _ % 50 == 0:
            print(_, len(locations))
        new_locations = set()
        for location in locations:
            x = _x(location)
            y = _y(location)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if not dx and not dy:
                        continue
                    if dx and dy:
                        continue
                    new_location = _num(
                        x + dx,
                        y + dy,
                    )
                    if orig_location(new_location, grid_height, grid_width) in rocks:
                        continue

                    new_locations.add(new_location)

        locations = new_locations
    # for loc in locations:
    #     print(_x(loc), _y(loc))
    return len(locations)


def run(inputs: str) -> int:
    global OFFSET

    rocks = set()
    grid_width, grid_height = None, 0
    starting_location = None

    for y, line in enumerate(inputs.splitlines()):
        characters = list(line)
        if not y:
            grid_width = len(characters)
            OFFSET *= grid_width
        for x, c in enumerate(characters):
            if c == "#":
                rocks.add(_num(x, y))
            elif c == "S":
                starting_location = _num(x, y)
        grid_height += 1

    logger.info(f"Starting location: {starting_location}")
    logger.info(f"Grid width: {grid_width}, grid height: {grid_height}")

    # breakpoint()

    return all_steps(starting_location, np.array(list(rocks)), grid_width, grid_height)
