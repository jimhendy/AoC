import numpy as np


def run(inputs):
    pos = np.array(inputs.split(",")).astype(int)
    return np.abs(pos - np.median(pos)).sum()