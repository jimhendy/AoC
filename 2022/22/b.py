import re
from collections import defaultdict, deque
from typing import Dict

from tools.point import Point2D

DIRECTIONS = deque(["right", "down", "left", "up"])
FACING_VALUE = {"right": 0, "left": 2, "up": 3, "down": 1}


def run(inputs: str):
    inputs = inputs.splitlines()
    board = inputs[:-2]

    open_tiles = set()
    walls = set()
    loop_tiles: Dict[str, Dict[Point2D, Point2D]] = defaultdict(dict)
    loop_directions: Dict[str, Dict[Point2D, Point2D]] = defaultdict(dict)

    for y, row in enumerate(board):

        for x, char in enumerate(row):
            if char == " ":
                continue

            if char == "#":
                walls.add(Point2D(x, y))
            elif char == ".":
                open_tiles.add(Point2D(x, y))

    side_length = len(board) // 3

    # Right Side 1 & Right Side 6
    for y in range(side_length):
        leaving = Point2D(max(p.x for p in open_tiles if p.y == y), y)
        entering = Point2D(
            max(p.x for p in open_tiles if p.y == 3 * side_length - 1 - y),
            3 * side_length - 1 - y,
        )

        beyond_leaving = leaving + Point2D.steps["right"]
        beyond_entering = entering + Point2D.steps["right"]

        can_leave = beyond_leaving not in walls
        can_enter = beyond_entering not in walls

        if can_leave and can_enter:
            loop_tiles["right"][beyond_leaving] = entering
            loop_tiles["right"][beyond_entering] = leaving
            loop_directions["right"][beyond_leaving] = "left"
            loop_directions["right"][beyond_entering] = "left"

    # Right Side 4 & Top Side 6
    for y in range(side_length):
        leaving = Point2D(
            max(p.x for p in open_tiles if p.y == y + side_length), y + side_length
        )
        entering = Point2D(
            4 * side_length - y - 1,
            min(p.y for p in open_tiles if p.x == 4 * side_length - y - 1),
        )

        beyond_leaving = leaving + Point2D.steps["right"]
        beyond_entering = entering + Point2D.steps["up"]

        can_leave = beyond_leaving not in walls
        can_enter = beyond_entering not in walls

        if can_leave and can_enter:
            loop_tiles["right"][beyond_leaving] = entering
            loop_tiles["up"][beyond_entering] = leaving
            loop_directions["right"][beyond_leaving] = "down"
            loop_directions["up"][beyond_entering] = "left"

    # Top Side 1 & Top Side 2
    for x in range(side_length):
        leaving = Point2D(
            side_length * 2 + x,
            min(p.y for p in open_tiles if p.x == side_length * 2 + x),
        )
        entering = Point2D(
            side_length - x - 1,
            min(p.y for p in open_tiles if p.x == side_length - x - 1),
        )

        beyond_leaving = leaving + Point2D.steps["up"]
        beyond_entering = entering + Point2D.steps["up"]

        can_leave = beyond_leaving not in walls
        can_enter = beyond_entering not in walls

        if can_leave and can_enter:
            loop_tiles["up"][beyond_leaving] = entering
            loop_tiles["up"][beyond_entering] = leaving
            loop_directions["up"][beyond_leaving] = "down"
            loop_directions["up"][beyond_entering] = "down"

    # Left Side 1 & Top Side 3
    for y in range(side_length):
        leaving = Point2D(min(p.x for p in open_tiles if p.y == y), y)
        entering = Point2D(
            side_length + x, min(p.y for p in open_tiles if p.x == side_length + x)
        )

        beyond_leaving = leaving + Point2D.steps["left"]
        beyond_entering = entering + Point2D.steps["up"]

        can_leave = beyond_leaving not in walls
        can_enter = beyond_entering not in walls

        if can_leave and can_enter:
            loop_tiles["left"][beyond_leaving] = entering
            loop_tiles["up"][beyond_entering] = leaving
            loop_directions["left"][beyond_leaving] = "down"
            loop_directions["up"][beyond_entering] = "right"

    # Left Side 2 & Bottom Side 6
    for y in range(side_length):
        leaving = Point2D(
            min(p.x for p in open_tiles if p.y == side_length + y), side_length + y
        )
        entering = Point2D(
            side_length * 4 - y - 1,
            max(p.y for p in open_tiles if p.x == side_length * 4 - y - 1),
        )

        beyond_leaving = leaving + Point2D.steps["left"]
        beyond_entering = entering + Point2D.steps["down"]

        can_leave = beyond_leaving not in walls
        can_enter = beyond_entering not in walls

        if can_leave and can_enter:
            loop_tiles["left"][beyond_leaving] = entering
            loop_tiles["down"][beyond_entering] = leaving
            loop_directions["left"][beyond_leaving] = "up"
            loop_directions["down"][beyond_entering] = "right"

    # Bootom Side 2 & Bottom Side 5
    for x in range(side_length):
        leaving = Point2D(x, max(p.y for p in open_tiles if p.x == x))
        entering = Point2D(
            side_length * 3 - 1 + x,
            max(p.y for p in open_tiles if p.x == side_length * 3 - 1 + x),
        )

        beyond_leaving = leaving + Point2D.steps["down"]
        beyond_entering = entering + Point2D.steps["down"]

        can_leave = beyond_leaving not in walls
        can_enter = beyond_entering not in walls

        if can_leave and can_enter:
            loop_tiles["down"][beyond_leaving] = entering
            loop_tiles["down"][beyond_entering] = leaving
            loop_directions["down"][beyond_leaving] = "up"
            loop_directions["down"][beyond_entering] = "up"

    # Bottom Side 3 & Left Side 5
    for x in range(side_length):
        leaving = Point2D(
            side_length + x, max(p.y for p in open_tiles if p.x == side_length + x)
        )
        entering = Point2D(
            min(p.x for p in open_tiles if p.y == side_length * 3 - x - 1),
            side_length * 3 - x - 1,
        )

        beyond_leaving = leaving + Point2D.steps["down"]
        beyond_entering = entering + Point2D.steps["left"]

        can_leave = beyond_leaving not in walls
        can_enter = beyond_entering not in walls

        if can_leave and can_enter:
            loop_tiles["down"][beyond_leaving] = entering
            loop_tiles["left"][beyond_entering] = leaving
            loop_directions["down"][beyond_leaving] = "right"
            loop_directions["left"][beyond_entering] = "up"

    print(loop_tiles)

    moves = map(int, re.findall(r"\d+", inputs[-1]))
    turns = iter(re.findall(r"[RL]", inputs[-1]))

    loc = Point2D(min(p.x for p in open_tiles if p.y == 0), 0)
    step = Point2D.steps["right"]

    import pdb

    pdb.set_trace()

    for num_steps in moves:
        print(f"Pre Move: {loc}, {DIRECTIONS[0]}")
        for _ in range(num_steps):
            new_loc = loc + step
            if new_loc in open_tiles:
                loc = new_loc
            elif new_loc in loop_tiles[DIRECTIONS[0]]:
                loc = loop_tiles[DIRECTIONS[0]][new_loc]
                new_direction = loop_directions[DIRECTIONS[0]][new_loc]
                while DIRECTIONS[0] != new_direction:
                    DIRECTIONS.rotate()
        print(f"Post Move: {loc}, {DIRECTIONS[0]}")
        try:
            rot = -1 if next(turns) == "R" else 1
            DIRECTIONS.rotate(rot)
            step = Point2D.steps[DIRECTIONS[0]]
        except StopIteration:
            print("No turns left")

    return 1_000 * (abs(loc.y) + 1) + 4 * (loc.x + 1) + FACING_VALUE[DIRECTIONS[0]]
