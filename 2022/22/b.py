import re
from collections import defaultdict, deque
from typing import Callable, Dict

from tools.point import Point2D

DIRECTIONS = deque(["right", "down", "left", "up"])
FACING_VALUE = {"right": 0, "left": 2, "up": 3, "down": 1}
OPPOSITES = {"down": "up", "up": "down", "left": "right", "right": "left"}


def run(inputs: str):  # sourcery skip: collection-into-set
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

    side_length = max(len(board) // 4, max(len(line) for line in board) // 4)

    def extract_from_x(
        x_lambda: Callable[[int], int], min_or_max: Callable
    ) -> Callable[[int], Point2D]:
        def func(i: int) -> Point2D:
            x = x_lambda(i)
            return Point2D(x=x, y=min_or_max(p.y for p in open_tiles if p.x == x))

        return func

    def extract_from_y(
        y_lambda: Callable[[int], int], min_or_max: Callable
    ) -> Callable[[int], Point2D]:
        def func(i: int) -> Point2D:
            y = y_lambda(i)
            return Point2D(
                x=min_or_max(p.x for p in open_tiles if p.y == y),
                y=y,
            )

        return func

    def configure_moves(
        leaving_lambda: Callable[[int], Point2D],
        entering_lambda: Callable[[int], Point2D],
        leaving_direction: str,
        entering_direction: str,
    ):
        """
        Add the loop data for a particular side exit.

        E.g. for the unfolded cube:
            11
            11
        223344
        223344
            5566
            5566

        Exiting the right of side 1 would enter from the right of side 6.
        Hence, this function is used with
        * leaving_direction="right"
        * entering_direction="left"

        With functions taking in an iterable of side length (2 in example) to create the Point2Ds
        e.g.

        leaving_lambda=lambda i: i
        entering_lambda=lambda i: side_length * 3 - 1 - i
        """
        if leaving_direction in {"up", "down"}:
            leaving_extract = extract_from_x
            leaving_min_max = min if leaving_direction == "up" else max
        else:
            leaving_extract = extract_from_y
            leaving_min_max = min if leaving_direction == "left" else max

        if entering_direction in {"up", "down"}:
            entering_extract = extract_from_x
            entering_min_max = min if entering_direction == "down" else max
        else:
            entering_extract = extract_from_y
            entering_min_max = min if entering_direction == "right" else max

        for i in range(side_length):
            leaving = leaving_extract(leaving_lambda, leaving_min_max)(i)
            entering = entering_extract(entering_lambda, entering_min_max)(i)

            beyond_leaving = leaving + Point2D.steps[leaving_direction]
            beyond_entering = entering + Point2D.steps[OPPOSITES[entering_direction]]

            can_leave = beyond_leaving not in walls
            can_enter = beyond_entering not in walls

            if can_leave and can_enter:
                loop_tiles[leaving_direction][beyond_leaving] = entering
                loop_directions[leaving_direction][beyond_leaving] = entering_direction

                loop_tiles[OPPOSITES[entering_direction]][beyond_entering] = leaving
                loop_directions[OPPOSITES[entering_direction]][
                    beyond_entering
                ] = OPPOSITES[leaving_direction]

    if side_length == 4:
        # Right of 1, right of 6
        configure_moves(
            leaving_direction="right",
            leaving_lambda=lambda i: i,
            entering_direction="left",
            entering_lambda=lambda i: 3 * side_length - 1 - i,
        )

        # Right of 4, top of 6
        configure_moves(
            leaving_direction="right",
            leaving_lambda=lambda i: side_length + i,
            entering_direction="down",
            entering_lambda=lambda i: 4 * side_length - 1 - i,
        )

        # Bottom of 6, left of 2
        configure_moves(
            leaving_direction="down",
            leaving_lambda=lambda i: 3 * side_length + i,
            entering_direction="right",
            entering_lambda=lambda i: 2 * side_length - 1 - i,
        )

        # Bottom of 5, bottom of 2
        configure_moves(
            leaving_direction="down",
            leaving_lambda=lambda i: 2 * side_length + i,
            entering_direction="up",
            entering_lambda=lambda i: side_length - 1 - i,
        )

        # Top of 1, top of 2
        configure_moves(
            leaving_direction="up",
            leaving_lambda=lambda i: 2 * side_length + i,
            entering_direction="down",
            entering_lambda=lambda i: side_length - 1 - i,
        )

        # Left of 1, top of 3
        configure_moves(
            leaving_direction="left",
            leaving_lambda=lambda i: i,
            entering_direction="down",
            entering_lambda=lambda i: side_length + i,
        )

        # Bottom of 3, left of 5
        configure_moves(
            leaving_direction="down",
            leaving_lambda=lambda i: side_length + i,
            entering_direction="right",
            entering_lambda=lambda i: 3 * side_length - 1 - i,
        )
    else:  # =====================================================================================
        # Right side 2, right side 4
        configure_moves(
            leaving_direction="right",
            leaving_lambda=lambda i: i,
            entering_direction="left",
            entering_lambda=lambda i: 3 * side_length - 1 - i,
        )

        # Right side 3, bottom side 2
        configure_moves(
            leaving_direction="right",
            leaving_lambda=lambda i: side_length + i,
            entering_direction="up",
            entering_lambda=lambda i: 2 * side_length + i,
        )

        # Right side 6, bottom side 4
        configure_moves(
            leaving_direction="right",
            leaving_lambda=lambda i: 3 * side_length + i,
            entering_direction="up",
            entering_lambda=lambda i: side_length + i,
        )

        # Top side 2, bottom side 6
        configure_moves(
            leaving_direction="up",
            leaving_lambda=lambda i: 2 * side_length + i,
            entering_direction="up",
            entering_lambda=lambda i: i,
        )

        # Top side 1, left side 6
        configure_moves(
            leaving_direction="up",
            leaving_lambda=lambda i: side_length + i,
            entering_direction="right",
            entering_lambda=lambda i: 3 * side_length + i,
        )

        # Left side 1, left side 5
        configure_moves(
            leaving_direction="left",
            leaving_lambda=lambda i: i,
            entering_direction="right",
            entering_lambda=lambda i: 3 * side_length - 1 - i,
        )

        # Left side 3, top side 5
        configure_moves(
            leaving_direction="left",
            leaving_lambda=lambda i: side_length + i,
            entering_direction="down",
            entering_lambda=lambda i: i,
        )

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
                new_direction = loop_directions[DIRECTIONS[0]][new_loc]
                while DIRECTIONS[0] != new_direction:
                    DIRECTIONS.rotate()
                step = Point2D.steps[new_direction]
        try:
            rot = -1 if next(turns) == "R" else 1
            DIRECTIONS.rotate(rot)
            step = Point2D.steps[DIRECTIONS[0]]
        except StopIteration:
            ...

    return 1_000 * (abs(loc.y) + 1) + 4 * (loc.x + 1) + FACING_VALUE[DIRECTIONS[0]]
