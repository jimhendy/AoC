import common
import numpy as np


def run(inputs):
    data = common.in_to_array(inputs)

    # We don't care about row or column so resize to flatten that
    data = data.reshape(data.shape[0], -1)

    # Index of the fewest zeros
    zeros = (data == 0).astype(int).sum(axis=1)
    index = zeros.argmin()

    unique, counts = np.unique(data[index], return_counts=True)
    counts = dict(zip(unique, counts))

    return counts[1] * counts[2]
