import numpy as np


def run(inputs: str) -> int:
    all_numbers = np.array(
        [list(map(int, line.split())) for line in inputs.splitlines()],
    )
    nums_1 = all_numbers[:, 0]
    nums_2 = all_numbers[:, 1]

    # Sort both arrays
    nums_1.sort()
    nums_2.sort()

    diffs = nums_1 - nums_2

    abs_diffs = np.abs(diffs)

    return np.sum(abs_diffs)
