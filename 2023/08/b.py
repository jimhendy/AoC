import math
from itertools import cycle


def steps_from_origin(
    origin: str,
    network: dict[str, dict[str, str]],
    directions: str,
) -> int:
    directions = cycle(directions)
    steps = 0
    location = origin
    while location[-1] != "Z":
        location = network[location][next(directions)]
        steps += 1
    return steps


def run(inputs: str) -> int:
    lines = inputs.splitlines()

    directions = lines[0]
    network = {}
    for line in lines[2:]:
        origin, destinations = line.split(" = ")
        destinations = [d.strip() for d in destinations[1:-1].split(",")]
        network[origin] = {"L": destinations[0], "R": destinations[1]}

    steps = [
        steps_from_origin(origin, network, directions)
        for origin in network
        if origin[-1] == "A"
    ]

    return math.lcm(*steps)
