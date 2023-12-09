from itertools import cycle


def run(inputs: str) -> int:
    lines = inputs.splitlines()

    directions = cycle(lines[0])
    network = {}
    for line in lines[2:]:
        origin, destinations = line.split(" = ")
        destinations = [d.strip() for d in destinations[1:-1].split(",")]
        network[origin] = {"L": destinations[0], "R": destinations[1]}

    steps = 0
    location = "AAA"
    while location != "ZZZ":
        location = network[location][next(directions)]
        steps += 1
    return steps
