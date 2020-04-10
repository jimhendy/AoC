import numpy as np


def run(inputs):
    n_elves = int(inputs)
    elves = np.arange(1, n_elves + 1)
    while elves.shape[0] > 1:
        print(elves.shape[0])
        if elves.shape[0] % 2 == 0:
            elves = elves.reshape(-1, 2)[:, 0]
        else:
            elves = np.hstack((elves[-1], elves[:-1].reshape(-1, 2)[:, 0]))
        pass
    return elves[0]
