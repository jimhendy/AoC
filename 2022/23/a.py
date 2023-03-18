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


def rect_area(locations: Points):
    min_x = min(elf.x for elf in locations)
    max_x = max(elf.x for elf in locations)
    min_y = min(elf.y for elf in locations)
    max_y = max(elf.y for elf in locations)
    return (max_x - min_x + 1) * (max_y - min_y + 1)


def parse_inputs(inputs: str) -> Points:
    points = set()
    for y, row in enumerate(inputs.splitlines()):
        for x, char in enumerate(row):
            if char == "#":
                points.add(Point2D(x=x, y=y))
    return points


def print_grid(locations: Points) -> None:
    min_x = min(elf.x for elf in locations)
    max_x = max(elf.x for elf in locations)
    min_y = min(elf.y for elf in locations)
    max_y = max(elf.y for elf in locations)
    s = ""
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            s += "#" if Point2D(x=x, y=y) in locations else "."
        s += "\n"
    print(s)
    print("=" * 30)


def run(inputs: str) -> int:

    locations = parse_inputs(inputs)
    preferred_dirs = ["up", "down", "left", "right"]

    for _ in range(10):
        # print_grid(locations)
        wants = wants_to_move(locations)
        destinations = proposed_destinations(wants, locations, preferred_dirs)
        move_elves(locations, destinations)
        preferred_dirs = preferred_dirs[1:] + preferred_dirs[:1]

    return rect_area(locations) - len(locations)
