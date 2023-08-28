import os
from collections import defaultdict


def steps(p1, p2):
    step = 1 if p2 > p1 else -1
    return range(p1, p2 + step, step)


def run(inputs):
    points = defaultdict(int)  # (x, y) -> num vents

    for l in inputs.replace(" ", "").split(os.linesep):
        (x1, y1), (x2, y2) = (i.split(",") for i in l.split("->"))
        x1, x2, y1, y2 = map(int, (x1, x2, y1, y2))

        if x1 == x2 or y1 == y2:
            for x in steps(x1, x2):
                for y in steps(y1, y2):
                    points[(x, y)] += 1
        else:
            x = steps(x1, x2)
            y = steps(y1, y2)
            for x, y in zip(x, y):
                points[(x, y)] += 1

    return sum([v >= 2 for v in points.values()])
