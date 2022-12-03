import os
import re

import numpy as np


def area(dims):
    x = dims[0] * dims[1]
    y = dims[0] * dims[2]
    z = dims[1] * dims[2]
    smallest = min([x, y, z])
    return 2 * x + 2 * y + 2 * z + smallest
    pass


def run(inputs):

    reg = re.compile("(\d+)x(\d+)x(\d+)")

    dims = np.array(
        [int(i) for line in inputs.split(os.linesep) for i in reg.findall(line)[0]]
    ).reshape(-1, 3)

    total = 0
    for pres_dims in dims:
        total += area(pres_dims)
        pass

    return total
