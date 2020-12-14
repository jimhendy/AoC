import os
import re

from constellation import Constellation, Point


def run(inputs):

    c = [
        Constellation(
            [
                Point(
                    *list(
                        map(
                            int, re.findall(r"(-?\d+),(-?\d+),(-?\d+),(-?\d+)", line)[0]
                        )
                    )
                )
            ]
        )
        for line in inputs.split(os.linesep)
    ]

    c = sorted(c, key=lambda x: x.points[0].x[0])

    n_c = None
    no_merge = set()

    while len(c) != n_c:
        ignore = set()
        print(len(c), len(no_merge))
        n_c = len(c)

        for i, ci in enumerate(c[:-1]):
            if i in ignore:
                continue
            ci_str = ci.__repr__()
            for j, cj in enumerate(c):
                if j <= i:
                    continue
                if j in ignore:
                    continue
                s = ci_str + "@" + cj.__repr__()
                if s in no_merge:
                    continue
                if ci.distance(cj) <= 3:
                    ci.combine(cj)
                    ignore.add(j)
                else:
                    no_merge.add(s)

        for i in sorted(ignore)[::-1]:
            c.pop(i)

    return len(c)
