import os
from pair import Pair


def run(inputs):
    pairs = [Pair.from_str(i) for i in inputs.split(os.linesep)]

    p = pairs[0]
    for pi in pairs[1:]:
        p = p + pi

    return p.magnitude()
