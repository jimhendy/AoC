import numpy as np


def run(inputs):
    directions = {
        "v": np.array([0, +1]),
        "<": np.array([-1, 0]),
        "^": np.array([0, -1]),
        ">": np.array([+1, 0]),
    }

    loc = np.array([0, 0])
    locs = {tuple(loc): 0}
    for move in list(inputs):
        loc += directions[move]
        locs[tuple(loc)] = 0
        pass

    return len(locs)
