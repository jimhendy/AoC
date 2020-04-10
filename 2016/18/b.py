import numba
import numpy as np
import tqdm

SAFE = 0
TRAP = 1
N_ROWS = 400000


@numba.njit
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

    return a, b, c


@numba.njit
def next_row(prev_row):
    TRAP_COMBOS = [
        np.array(i)
        for i in [
            (TRAP, TRAP, SAFE),
            (SAFE, TRAP, TRAP),
            (TRAP, SAFE, SAFE),
            (SAFE, SAFE, TRAP),
        ]
    ]
    new = np.full_like(prev_row, SAFE)
    for i in range(len(prev_row)):
        prev = get_prev_tiles(prev_row, i)
        for tc in TRAP_COMBOS:
            if np.array_equal(prev, tc):
                new[i] = TRAP
    return new


def run(inputs):
    first_row = np.array([{".": SAFE, "^": TRAP}.get(i) for i in list(inputs)])
    rows = [first_row]
    for i in tqdm.tqdm(range(N_ROWS - 1)):
        rows.append(next_row(rows[i]))

    return (N_ROWS * first_row.shape[0]) - np.array(rows).sum()
