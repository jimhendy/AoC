import os

from pair import Pair


def run(inputs):
    pairs = [Pair.from_str(i) for i in inputs.split(os.linesep)]

    max_mag = 0
    for xi, x in enumerate(pairs):
        for yi, y in enumerate(pairs):
            if xi == yi:
                continue
            m = (x + y).magnitude()
            max_mag = max(m, max_mag)

    return max_mag
