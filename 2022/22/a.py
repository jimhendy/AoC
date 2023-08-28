import re
from collections import defaultdict, deque

from tools.point import Point2D

DIRECTIONS = deque(["right", "down", "left", "up"])
FACING_VALUE = {"right": 0, "left": 2, "up": 3, "down": 1}


def run(inputs: str):
    inputs = inputs.splitlines()
    board = inputs[:-2]

    open_tiles = set()
    walls = set()
    loop_tiles: dict[str, dict[Point2D, Point2D]] = defaultdict(dict)

    for y, row in enumerate(board):
        for x, char in enumerate(row):
            if char == " ":
                continue

            if char == "#":
                walls.add(Point2D(x, y))
            elif char == ".":
                open_tiles.add(Point2D(x, y))

        rightmost = Point2D(max(p.x for p in open_tiles if p.y == y), y)
        leftmost = Point2D(min(p.x for p in open_tiles if p.y == y), y)

        beyond_rightmost = rightmost + Point2D.steps["right"]
        beyond_leftmost = leftmost + Point2D.steps["left"]

        can_go_right = beyond_rightmost not in walls
        can_go_left = beyond_leftmost not in walls

        if can_go_right and can_go_left:
            loop_tiles["right"][beyond_rightmost] = leftmost
            loop_tiles["left"][beyond_leftmost] = rightmost

    for x in range(len(board[0])):
        topmost = Point2D(x, min(p.y for p in open_tiles if p.x == x))
        bottommost = Point2D(x, max(p.y for p in open_tiles if p.x == x))

        beyond_topmost = topmost + Point2D.steps["up"]
        beyond_bottommost = bottommost + Point2D.steps["down"]

        can_go_up = beyond_topmost not in walls
        can_go_down = beyond_bottommost not in walls

        if can_go_up and can_go_down:
            loop_tiles["up"][beyond_topmost] = bottommost
            loop_tiles["down"][beyond_bottommost] = topmost

    moves = map(int, re.findall(r"\d+", inputs[-1]))
    turns = iter(re.findall(r"[RL]", inputs[-1]))

    loc = Point2D(min(p.x for p in open_tiles if p.y == 0), 0)
    step = Point2D.steps["right"]

    for num_steps in moves:
        for _ in range(num_steps):
            new_loc = loc + step
            if new_loc in open_tiles:
                loc = new_loc
            elif new_loc in loop_tiles[DIRECTIONS[0]]:
                loc = loop_tiles[DIRECTIONS[0]][new_loc]
        try:
            rot = -1 if next(turns) == "R" else 1
            DIRECTIONS.rotate(rot)
            step = Point2D.steps[DIRECTIONS[0]]
        except StopIteration:
            print("No turns left")

    return 1_000 * (abs(loc.y) + 1) + 4 * (loc.x + 1) + FACING_VALUE[DIRECTIONS[0]]
