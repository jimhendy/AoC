import os


def step(east, south, width, height):
    next_east = set()
    next_south = set()

    for current in east:
        dest = (
            (current[0] + 1, current[1]) if current[0] < width - 1 else (0, current[1])
        )
        if dest not in east and dest not in south:
            next_east.add(dest)
        else:
            next_east.add(current)

    for current in south:
        dest = (
            (current[0], current[1] + 1) if current[1] < height - 1 else (current[0], 0)
        )
        if dest not in next_east and dest not in south:
            next_south.add(dest)
        else:
            next_south.add(current)

    return next_east, next_south


def run(inputs):
    east = set()
    south = set()

    for i, line in enumerate(inputs.split(os.linesep)):
        for j, char in enumerate(line):
            if char == ">":
                east.add((j, i))
            elif char == "v":
                south.add((j, i))
            elif char != ".":
                msg = f"Unexpected map character: {char}"
                raise RuntimeError(msg)

    width = j + 1
    height = i + 1
    n_steps = 0

    while True:
        next_east, next_south = step(east, south, width, height)
        n_steps += 1
        if len(next_east | east) == len(east) and len(next_south | south) == len(south):
            return n_steps
        else:
            east, south = next_east, next_south
