import numba as nb
import numpy as np
from loguru import logger

STEPS = 26501365


@nb.njit
def _location_in_original_grid(
    location: complex, grid_width: int, grid_height: int
) -> complex:
    return complex(location.real % grid_width, location.imag % grid_height)


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

    # Check if there are any rocks directly up, down, left or right of the starting position
    for step in [1j, -1j, 1, -1]:
        position = starting_location
        while True:
            position += step
            if position in rocks:
                logger.error(
                    f"Found rock at {position}. There is not a clear path to the edge of the grid in the direction {step}"
                )
            if position.real < 0 or position.imag < 0:
                break
            if position.real == grid_width:
                break
            if position.imag == grid_height:
                break

    # Find how many free spaces (".") are accessible from the starting position on even or odd steps
    even_spaces = {starting_location}
    odd_spaces = set()
    step_num = 0
    previous_spaces = even_spaces

    while previous_spaces:
        step_num += 1
        incumbent = odd_spaces if step_num % 2 else even_spaces
        new_spaces = set()
        for position in previous_spaces:
            for step in [1j, -1j, 1, -1]:
                new_position = position + step
                if new_position.real < 0 or new_position.imag < 0:
                    continue
                if new_position.real == grid_width or new_position.imag == grid_height:
                    continue
                if new_position in rocks:
                    continue
                if new_position in incumbent:
                    continue
                incumbent.add(new_position)
                new_spaces.add(new_position)

        previous_spaces = new_spaces

    logger.info(f"Even spaces: {len(even_spaces)}, odd spaces: {len(odd_spaces)}")

    # How many full tiles will be go up, down, left or right from the starting position in the STEPS steps
    full_tiles = {}
    remainders = {}
    print(f"Starting location: {starting_location}")
    for step in [1j, -1j, 1, -1]:

        # How many steps from the starting position to the edge of the original grid
        position = starting_location

        grid_size = grid_width if step.real else grid_height
        edge = 0 if (step.real + step.imag) < 0 else grid_size - 1
        start_loc = starting_location.real if step.real else starting_location.imag
        steps_to_edge = abs(edge - start_loc)

        print(f"Steps to edge: {steps_to_edge} for {step}")

        steps_after_edge = max(STEPS - steps_to_edge, 0)
        full, remainder = divmod(steps_after_edge, grid_size)

        full_tiles[step] = int(full)
        remainders[step] = int(remainder)

        print(f"Full: {full}, remainder: {remainder}")

    max_width = full_tiles[1] + full_tiles[-1]
    max_height = full_tiles[1j] + full_tiles[-1j]

    total_full = 0
    width = 1
    for _ in range(full_tiles[1]):
        total_full += 2 * width
        width += 2

    total_full += max_width

    # Add up the contributions fro the remainders

    if STEPS % 2:
        print("Odd")
        return len(odd_spaces) * total_full
    else:
        print("Even")
        return len(even_spaces) * total_full

    print(f"Max width: {max_width}, max height: {max_height}")

    return 9
