import os
from collections import defaultdict
from itertools import combinations


def run(inputs):

    sizes = [int(i) for i in inputs.split(os.linesep)]

    count = 0
    counts = defaultdict(int)
    for n in range(len(sizes)):
        for c in combinations(sizes, n):
            if sum(c) == 150:
                count += 1
                counts[n] += 1
                pass
            pass
        if len(counts):
            return counts[n]
        pass

    pass
