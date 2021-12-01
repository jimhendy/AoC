import os


def run(inputs):
    depths = list(map(int, inputs.split(os.linesep)))
    return sum(x < y for x, y in zip(depths, depths[3:]))
