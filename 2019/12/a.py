import os

import common
import numpy as np
from moon import Moon


def run(inputs):

    moons = [Moon(ps) for ps in inputs.split(os.linesep)]
    n_steps = 1000

    for s in range(1, n_steps + 1):
        for i, mi in enumerate(moons):
            for j, mj in enumerate(moons[i + 1 :]):
                common.apply_gravity(mi, mj)
                pass
            pass
        [m.update_position() for m in moons]
        print(f"After {s} steps:")
        [print(m.print_data()) for m in moons]
        print()
        pass

    return np.sum([m.energy() for m in moons])
