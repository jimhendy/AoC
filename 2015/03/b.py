import numpy as np


def run(inputs):
    directions = {
        "v": np.array([0, +1]),
        "<": np.array([-1, 0]),
        "^": np.array([0, -1]),
        ">": np.array([+1, 0]),
    }

    loc = [np.array([0, 0]), np.array([0, 0])]
    locs = {tuple(loc[0]): 0}

    chars = list(inputs)

    for i in range(0, len(inputs), 2):
        loc[0] += directions[chars[i]]
        loc[1] += directions[chars[i + 1]]

        locs[tuple(loc[0])] = 0
        locs[tuple(loc[1])] = 0

    return len(locs)
