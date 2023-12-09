import os

import common
import numpy as np
from moon import Moon


def get_status(moons, axis):
    return "-".join(
        [
            str(i)
            for i in (
                [m.position[axis] for m in moons] + [m.velocity[axis] for m in moons]
            )
        ],
    )


def check_hist(hist, moons, axis):
    status = get_status(moons, axis)
    if status in hist:
        return True
    else:
        hist.add(status)
        return False
    return None


def run(inputs):
    axis_frequencies = []

    # Do each axis alone
    for a in range(3):
        moons = [Moon(ps) for ps in inputs.split(os.linesep)]
        history = set()

        s = 0
        check_hist(history, moons, a)

        while True:
            s += 1
            for i, mi in enumerate(moons):
                for _j, mj in enumerate(moons[i + 1 :]):
                    common.apply_gravity(mi, mj)
            [m.update_position() for m in moons]

            if s % 10000 == 0:
                print(f"Iteration: {s}")

            if check_hist(history, moons, axis=a):
                axis_frequencies.append(s)
                break

    return np.lcm.reduce(axis_frequencies)
