import copy
import os


def get_neighbours(y, x, lights):
    total = 0
    if y:
        row = lights[y - 1]
        if x:
            total += row[x - 1] == "#"
        total += row[x] == "#"
        if x < len(row) - 1:
            total += row[x + 1] == "#"
    if y < len(lights) - 1:
        row = lights[y + 1]
        if x:
            total += row[x - 1] == "#"
        total += row[x] == "#"
        if x < len(row) - 1:
            total += row[x + 1] == "#"
    if x:
        total += lights[y][x - 1] == "#"
    if x < len(lights[0]) - 1:
        total += lights[y][x + 1] == "#"
    return total


def update(lights):
    orig = copy.deepcopy(lights)
    size = len(lights) - 1
    for y_i, y in enumerate(lights):
        for x_i, x in enumerate(y):
            if (
                (x_i == 0 and y_i == 0)
                or (x_i == 0 and y_i == size)
                or (x_i == size and y_i == 0)
                or (x_i == size and y_i == size)
            ):
                continue

            on = x == "#"
            n_neighbours = get_neighbours(y_i, x_i, orig)
            if on:
                if n_neighbours not in [2, 3]:
                    lights[y_i][x_i] = "."
            else:
                if n_neighbours == 3:
                    lights[y_i][x_i] = "#"

    return lights


def run(inputs):
    lights = [list(i) for i in inputs.split(os.linesep)]

    size = len(lights) - 1
    lights[0][0] = "#"
    lights[0][size] = "#"
    lights[size][0] = "#"
    lights[size][size] = "#"

    for _i in range(100):
        [print("".join(l)) for l in lights]
        print()
        lights = update(lights)
    [print("".join(l)) for l in lights]
    print()
    return sum([i.count("#") for i in lights])
