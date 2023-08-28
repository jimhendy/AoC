import os

import numpy as np

KEYPAD = np.array([list(l) for l in ["00100", "02340", "56789", "0ABC0", "00D00"]]).T

steps = {
    "L": np.array([-1, 0]),
    "R": np.array([+1, 0]),
    "U": np.array([0, -1]),
    "D": np.array([0, +1]),
}


def move(step_dir, current_pos):
    new_pos = np.clip(current_pos + steps[step_dir], a_min=0, a_max=KEYPAD.shape[0] - 1)
    new_char = KEYPAD[tuple(new_pos)]
    if new_char == "0":
        return current_pos
    else:
        return new_pos


def run(inputs):
    pos = np.argwhere(KEYPAD == "5")[0]
    results = []

    for line in inputs.split(os.linesep):
        for s in line:
            pos = move(s, pos)
        results.append(KEYPAD[tuple(pos)])

    return "".join(results)
