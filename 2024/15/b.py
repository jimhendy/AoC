from typing import Literal

from tools.inputs import parse_grid

EMPTY = "."
LEFT_BOX = "["
RIGHT_BOX = "]"
WALL = "#"


def move_boxes(
    grid: dict[complex:str],
    location: complex,
    direction: complex,
) -> list[complex] | Literal[False]:
    """Return a list of **original** box locations that can be moved.

    If a box cannot be moved, return False.

    If we are pushing left or right, things are pretty simple.
    If moving up or down, we need also move the other half of any boxes we push.
    """
    if grid[location] == EMPTY:
        return []
    if grid[location] == WALL:
        return False
    if direction.real:
        down_stream = move_boxes(grid, location + direction, direction)
        if down_stream is False:
            return False
        return [location] + down_stream
    is_left = grid[location] == LEFT_BOX
    other_loc = location + (1 if is_left else -1)
    down_stream = move_boxes(grid, location + direction, direction)
    if down_stream is False:
        return False
    down_stream_other = move_boxes(grid, other_loc + direction, direction)
    if down_stream_other is False:
        return False
    return [location, other_loc] + down_stream + down_stream_other


def widen_grid(grid: str) -> str:
    """If the tile is #, the new map contains ## instead.
    If the tile is O, the new map contains [] instead.
    If the tile is ., the new map contains .. instead.
    If the tile is @, the new map contains @. instead.
    """
    return "\n".join(
        "".join({"#": "##", "O": "[]", ".": "..", "@": "@."}.get(c, c) for c in line)
        for line in grid.split("\n")
    )


def run(inputs: str) -> int:
    grid, commands = inputs.split("\n\n")
    grid = widen_grid(grid)
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

        if grid[next_pos] in (LEFT_BOX, RIGHT_BOX):
            boxes = move_boxes(grid, next_pos, direction)
            if boxes is False:
                continue
            boxes = set(boxes)

            # Order of the shift matters, sort in -direction
            if command == "<":
                boxes = sorted(boxes, key=lambda b: b.real, reverse=False)
            elif command == ">":
                boxes = sorted(boxes, key=lambda b: b.real, reverse=True)
            elif command == "^":
                boxes = sorted(boxes, key=lambda b: b.imag, reverse=False)
            elif command == "v":
                boxes = sorted(boxes, key=lambda b: b.imag, reverse=True)

            for box in boxes:
                grid[box + direction] = grid[box]
                grid[box] = EMPTY

        robot = next_pos

    # Find the GPS of all boxes
    boxes = [k for k, v in grid.items() if v == LEFT_BOX]
    return sum(100 * b.imag + b.real for b in boxes)
