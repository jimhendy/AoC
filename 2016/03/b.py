import os
import numpy as np


def run(inputs):

    sides = np.array([i.split() for i in inputs.split(os.linesep)]).astype(int)

    sides = sides.T.reshape(-1, 3)

    all_indices = set(range(sides.shape[1]))
    valid = []
    for input_1 in range(sides.shape[1]):
        for input_2 in range(input_1 + 1, sides.shape[1]):
            remaining_side = list(all_indices - set([input_1, input_2]))[0]
            this_valid = np.greater(
                sides[:, (input_1, input_2)].sum(axis=1), sides[:, remaining_side]
            )
            valid.append(this_valid)

    return np.all(valid, axis=0).sum()
