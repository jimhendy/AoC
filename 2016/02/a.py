import os

import numpy as np

KEYPAD = np.arange(1, 10).reshape(3, 3).T

steps = {
    "L": np.array([-1, 0]),
    "R": np.array([+1, 0]),
    "U": np.array([0, -1]),
    "D": np.array([0, +1]),
}


def move(step_dir, current_pos):
    return np.clip(current_pos + steps[step_dir], a_min=0, a_max=KEYPAD.shape[0] - 1)


def run(inputs):
    pos = np.argwhere(KEYPAD == 5)[0]
    results = []

    for line in inputs.split(os.linesep):
        for s in line:
            pos = move(s, pos)
        results.append(KEYPAD[tuple(pos)])

    return "".join(map(str, results))
