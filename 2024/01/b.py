import numpy as np


def run(inputs: str) -> int:
    all_numbers = np.array(
        [list(map(int, line.split())) for line in inputs.splitlines()]
    )
    nums_1 = all_numbers[:, 0]
    nums_2 = all_numbers[:, 1]

    total = 0
    for i in nums_1:
        total += i * np.sum(nums_2 == i)

    return total
