from collections import defaultdict

from tools.point import Point2D

Points = set[Point2D]

MOVES = {
    "up": ["up-left", "up", "up-right"],
    "down": ["down-left", "down", "down-right"],
    "left": ["up-left", "left", "down-left"],
    "right": ["up-right", "right", "down-right"],
}


def wants_to_move(locations: Points) -> Points:
    wants = []
    for loc in locations:
        for neighbour in loc.nb8():
            if neighbour in locations:
                wants.append(loc)
                break
    return wants


def all_empty(location: Point2D, locations: Points, direction: str) -> bool:
    return all(location.step(step) not in locations for step in MOVES[direction])


def proposed_destinations(
    wants_to_move: Points, locations: Points, directions: list[str]
) -> dict[Point2D, list[Point2D]]:
    destinations = defaultdict(list)
    for loc in wants_to_move:
        for dir in directions:
            if all_empty(loc, locations, dir):
                destinations[loc.step(dir)].append(loc)
                break
    return destinations


def move_elves(locations: Points, destinations: dict[Point2D, list[Point2D]]) -> None:
    for dest, froms in destinations.items():
        if len(froms) == 1:
            locations.remove(froms[0])
            locations.add(dest)


def parse_inputs(inputs: str) -> Points:
    points = set()
    for y, row in enumerate(inputs.splitlines()):
        for x, char in enumerate(row):
            if char == "#":
                points.add(Point2D(x=x, y=y))
    return points


def run(inputs: str) -> int:

    locations = parse_inputs(inputs)
    preferred_dirs = ["up", "down", "left", "right"]

    round_num = 1
    while True:
        wants = wants_to_move(locations)
        if not len(wants):
            break
        destinations = proposed_destinations(wants, locations, preferred_dirs)
        move_elves(locations, destinations)
        preferred_dirs = preferred_dirs[1:] + preferred_dirs[:1]
        round_num += 1

    return round_num
