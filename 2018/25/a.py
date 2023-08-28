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
                            int,
                            re.findall(r"(-?\d+),(-?\d+),(-?\d+),(-?\d+)", line)[0],
                        ),
                    ),
                ),
            ],
        )
        for line in inputs.split(os.linesep)
    ]

    n_c = None
    no_merge = set()

    while len(c) != n_c:
        merged = set()
        print(len(c))
        n_c = len(c)

        for i, ci in enumerate(c[:-1]):
            if i in merged:
                continue
            ci_str = ci.__repr__()
            for j, cj in enumerate(c):
                if j <= i or j in merged:
                    continue
                s = ci_str + "@" + cj.__repr__()
                if s in no_merge:
                    continue
                if ci.distance(cj) <= 3:
                    ci.combine(cj)
                    merged.add(j)
                else:
                    no_merge.add(s)

        for i in sorted(merged)[::-1]:
            c.pop(i)

    return n_c
