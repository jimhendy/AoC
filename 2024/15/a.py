from typing import Literal

from tools.inputs import parse_grid

EMPTY = "."
BOX = "O"
WALL = "#"

CACHE = {}


def box_destination(
    grid: dict[complex:str],
    box_location: complex,
    direction: complex,
) -> complex | Literal[False]:
    """
    The destination of the pushed box.

    If multiple boxes are pushed, the destination is the next empty cell in the
    direction of the push.

    Boxes cannot be pushed- through walls.

    If the box cannot be moved, return False.
    """
    cache_key = (str(grid), box_location, direction)
    if cache_key in CACHE:
        return CACHE[cache_key]

    destination = box_location + direction
    while grid[destination] == BOX:
        destination += direction
    if grid[destination] == WALL:
        CACHE[cache_key] = False
        return False
    CACHE[cache_key] = destination
    return destination


def run(inputs: str) -> int:
    grid, commands = inputs.split("\n\n")
    commands = "".join(commands.split())
    grid = parse_grid(grid)

    robot = next(k for k, v in grid.items() if v == "@")
    grid[robot] = EMPTY

    for command in commands:
        direction = {
            "<": complex(-1, 0),
            ">": complex(1, 0),
            "^": complex(0, -1),
            "v": complex(0, 1),
        }[command]
        next_pos = robot + direction
        if grid[next_pos] == WALL:
            continue

        if grid[next_pos] == BOX:
            box_dest = box_destination(grid, next_pos, direction)
            if not box_dest:
                continue
            grid[next_pos] = EMPTY
            grid[box_dest] = BOX

        robot = next_pos

    # Find the GPS of all boxes
    boxes = [k for k, v in grid.items() if v == BOX]
    return sum(100 * b.imag + b.real for b in boxes)
