import os
import numpy as np

import common
from moon import Moon


def get_status(moons, axis):
    return "-".join(
        [
            str(i)
            for i in (
                [m.position[axis] for m in moons] + [m.velocity[axis] for m in moons]
            )
        ]
    )


def check_hist(hist, moons, axis):
    status = get_status(moons, axis)
    if status in hist:
        return True
    else:
        hist.add(status)
        return False
    pass


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
                for j, mj in enumerate(moons[i + 1 :]):
                    common.apply_gravity(mi, mj)
                    pass
                pass
            [m.update_position() for m in moons]

            if s % 10000 == 0:
                print(f"Iteration: {s}")
                pass

            if check_hist(history, moons, axis=a):
                axis_frequencies.append(s)
                break

            pass
        pass

    lcm = np.lcm.reduce(axis_frequencies)

    return lcm
