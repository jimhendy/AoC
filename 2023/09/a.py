import numpy as np


def predicted_delta(nums: np.ndarray) -> int:
    diffs = np.diff(nums)
    if np.all(diffs == 0):
        return 0
    return diffs[-1] + predicted_delta(diffs)


def run(inputs: str) -> int:
    total = 0
    for line in inputs.splitlines():
        nums = [int(x) for x in line.split()]
        nv = nums[-1] + predicted_delta(nums)
        total += nv

    return total
