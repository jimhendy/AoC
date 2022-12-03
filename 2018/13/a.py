import os

import numpy as np
from cart import Cart


def run(inputs):
    track = np.array([list(line) for line in inputs.split(os.linesep)])
    carts = []
    for r, row in enumerate(track):
        for c, char in enumerate(row):
            if char.lower() in ["v", ">", "<", "^"]:
                carts.append(Cart(np.array((r, c)), track))

    count = 0
    while True:
        crash = False
        for c in sorted(carts):
            c.step()
            if len(set([c.loc_as_str() for c in carts])) != len(carts):
                crash = True
                break
        if crash:
            break
        count += 1

    locs = []
    for c in carts:
        if not c.loc_as_str() in locs:
            locs.append(c.loc_as_str())
        else:
            return f"{c.loc[1]},{c.loc[0]}"
