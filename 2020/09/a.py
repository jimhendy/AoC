import os
import itertools

def run(inputs):
    nums = list(map(int, inputs.split(os.linesep)))
    preamble = 25

    for i,target in enumerate(nums[preamble:]):
        possibles = nums[i: i+preamble]
        found = False
        for a,b in itertools.combinations(possibles, 2):
            if a + b == target:
                found = True
                break
        if found:
            continue
        return target
