import os
import itertools


def run(inputs):
    nums = list(map(int, inputs.split(os.linesep)))
    preamble = 25

    for i, target in enumerate(nums[preamble:]):
        possibles = nums[i : i + preamble]
        found = False
        for a, b in itertools.combinations(possibles, 2):
            if a + b == target:
                found = True
                break
        if found:
            continue
        break

    target_i = i + preamble

    for start in range(target_i - 1):
        for end in range(start, target_i):
            considered = nums[start:end]
            total = sum(considered)
            if total == target:
                return min(considered) + max(considered)
            elif total > target:
                break
