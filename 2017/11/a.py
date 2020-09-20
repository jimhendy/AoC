import numpy as np

def run(inputs):
    commands = inputs.split(',')

    steps = {
        'n': np.array([0, 1, -1]),
        's': np.array([0, -1, 1]),
        'ne': np.array([1, 0, -1]),
        'nw': np.array([-1, 1, 0]),
        'se': np.array([1, -1, 0]),
        'sw': np.array([-1, 0, 1])
    }

    pos = np.array([0,0,0])

    for c in commands:
        pos += steps[c]

    distance = np.sum(np.abs(pos)) / 2

    return distance