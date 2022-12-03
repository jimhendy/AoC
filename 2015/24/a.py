import itertools
import os

import numpy as np


def subsets_that_sum(possibles, target, subset_size=None):

    if subset_size is None:
        Min = 1
        Max = len(possibles)
    else:
        Min = subset_size
        Max = subset_size + 1

    for section_size in range(Min, Max):
        for sec in (
            s
            for s in itertools.combinations(possibles, section_size)
            if sum(s) == target
        ):
            yield sec


def qe(packages):
    return np.product(packages)


def run(inputs):

    n_groups = 3
    weights = set(map(int, inputs.split(os.linesep)))
    group_sum = sum(weights) / n_groups

    results = []

    for g1_size in range(1, len(weights)):

        if len(results):
            break

        for g1 in subsets_that_sum(weights, group_sum, subset_size=g1_size):

            for g2 in subsets_that_sum([w for w in weights if w not in g1], group_sum):
                results.append(g1)
                break

    best = sorted(results, key=lambda x: qe(x))[0]

    return qe(best)
