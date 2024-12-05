import numpy as np


def is_monotonic(nums: list[int]) -> bool:
    return np.all(np.diff(nums) >= 0) or np.all(np.diff(nums) <= 0)


def all_gaps(nums: list[int], min_: int, max_: int) -> bool:
    return all(min_ <= gap <= max_ for gap in np.abs(np.diff(nums)))


def test(nums: list[int]) -> bool:
    if not is_monotonic(nums):
        return False
    if not all_gaps(nums, min_=1, max_=3):
        return False
    return True


def run(inputs: str) -> int:
    num_safe = 0
    for nums in [list(map(int, line.split())) for line in inputs.splitlines()]:
        for remove_index in range(len(nums)):
            num_copy = nums.copy()
            num_copy.pop(remove_index)
            if test(num_copy):
                num_safe += 1
                break
    return num_safe
