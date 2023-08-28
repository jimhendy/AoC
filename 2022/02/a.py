import numpy as np


def run(inputs):
    str_data = np.array(
        [line.split() for line in inputs.splitlines()],
        dtype=np.dtype("U1"),
    )

    data = np.stack(
        (
            np.vectorize({"A": 1, "B": 2, "C": 3}.get)(str_data[:, 0]),
            np.vectorize({"X": 1, "Y": 2, "Z": 3}.get)(str_data[:, 1]),
        ),
        axis=1,
    )

    abs_diff = np.abs(data[:, 0] - data[:, 1])

    max_wins = abs_diff == 1
    min_wins = abs_diff == 2
    draws = abs_diff == 0

    we_have_max = data[:, 1] > data[:, 0]

    we_win = np.logical_or(
        np.logical_and(we_have_max, max_wins),
        np.logical_and(~we_have_max, min_wins),
    )

    return data[:, 1].sum() + we_win.sum() * 6 + draws.sum() * 3
