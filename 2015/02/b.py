import os
import re

import numpy as np


def length(dims):
    s_dims = sorted(dims)
    ribbon = 2 * (s_dims[0] + s_dims[1])
    ribbon += dims[0] * dims[1] * dims[2]
    return ribbon


def run(inputs):
    reg = re.compile(r"(\d+)x(\d+)x(\d+)")

    dims = np.array(
        [int(i) for line in inputs.split(os.linesep) for i in reg.findall(line)[0]],
    ).reshape(-1, 3)

    total = 0
    for pres_dims in dims:
        total += length(pres_dims)

    return total
