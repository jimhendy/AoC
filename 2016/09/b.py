import os
import re

import numpy as np


def run(inputs):
    data = "".join(inputs.split(os.linesep))
    marker_reg = re.compile(r"\((\d+)x(\d+)\)")

    multiples = np.ones(len(data))
    for match in marker_reg.finditer(data):
        start, end = match.span()
        multiples[start:end] = 0

        n_chars, repeats = list(map(int, match.groups()))
        multiples[end : end + n_chars] *= repeats

        pass

    return multiples.sum()
