import os

import numpy as np


def run(inputs):
    inputs = inputs.split(os.linesep)
    rights = [1, 3, 5, 7, 1]
    downs = [1, 1, 1, 1, 2]

    data = []
    for r, d in zip(rights, downs):
        trees = sum(
            [
                inputs[row][col % len(inputs[0])] == "#"
                for row, col in zip(range(0, len(inputs), d), range(0, int(9e99), r))
            ]
        )
        data.append(trees)

    return np.prod(data)
