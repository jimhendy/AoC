import numpy as np
from enum import Enum

SAFE = "."
TRAP = "^"
N_ROWS = 40

TRAP_COMBOS = [
    "".join(i)
    for i in [
        (TRAP, TRAP, SAFE),
        (SAFE, TRAP, TRAP),
        (TRAP, SAFE, SAFE),
        (SAFE, SAFE, TRAP),
    ]
]


def get_prev_tiles(tiles, pos):
    b = tiles[pos]

    if pos - 1 < 0:
        a = SAFE
    else:
        a = tiles[pos - 1]

    if pos + 1 >= tiles.shape[0]:
        c = SAFE
    else:
        c = tiles[pos + 1]

    return "".join((a, b, c))


def next_row(prev_row):
    new = np.full_like(prev_row, SAFE)
    for i in range(len(prev_row)):
        prev = get_prev_tiles(prev_row, i)
        if prev in TRAP_COMBOS:
            new[i] = TRAP
    return new


def run(inputs):
    first_row = np.array(list(inputs))
    rows = [first_row]
    for i in range(N_ROWS - 1):
        rows.append(next_row(rows[i]))
    total = 0
    for r in rows:
        for t in r:
            if t == SAFE:
                total += 1
    return total
