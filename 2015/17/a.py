import os
from itertools import combinations


def run(inputs):
    sizes = [int(i) for i in inputs.split(os.linesep)]

    count = 0
    for n in range(len(sizes)):
        for c in combinations(sizes, n):
            if sum(c) == 150:
                count += 1

    return count
