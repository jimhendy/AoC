import operator
from itertools import product

OPS = (
    operator.add,
    operator.mul,
)


def run(inputs: str) -> int:
    total = 0
    for line in inputs.splitlines():
        target, nums = line.split(":")
        target = int(target)
        nums = list(map(int, nums.split()))
        for ops in product(OPS, repeat=len(nums) - 1):
            left = nums[0]
            for right, op in zip(nums[1:], ops, strict=True):
                left = op(left, right)
            if left == target:
                total += target
                break

    return total
