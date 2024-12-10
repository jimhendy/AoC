import math
import operator
from collections.abc import Generator

import tqdm


def concat(left: int, right: int) -> int:
    len_right = int(math.log10(right)) + 1
    return left * 10**len_right + right


OPS = (
    operator.add,
    operator.mul,
    concat,
)


def all_possible_nums(nums: tuple[int, ...]) -> Generator[int, None, None]:
    if len(nums) == 1:
        yield nums[0]
        return

    left = nums[0]
    right = nums[1]
    for op in OPS:
        combination = op(left, right)
        yield from all_possible_nums((combination,) + nums[2:])


def run(inputs: str) -> int:
    total = 0
    for line in tqdm.tqdm(inputs.splitlines()):
        target, nums = line.split(":")
        target = int(target)
        nums = tuple(map(int, nums.split()))
        if target in all_possible_nums(nums):
            total += target

    return total
