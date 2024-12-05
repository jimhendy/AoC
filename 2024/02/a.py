import numpy as np


def is_monotonic(nums: list[int]) -> bool:
    return np.all(np.diff(nums) >= 0) or np.all(np.diff(nums) <= 0)


def all_gaps(nums: list[int], min_: int, max_: int) -> bool:
    return all(min_ <= gap <= max_ for gap in np.abs(np.diff(nums)))


def run(inputs: str) -> int:
    num_safe = 0
    for nums in [list(map(int, line.split())) for line in inputs.splitlines()]:
        if not is_monotonic(nums):
            continue
        if not all_gaps(nums, min_=1, max_=3):
            continue
        num_safe += 1
    return num_safe
