import os
from collections import defaultdict


def run(inputs):
    initial, _, *alteration_inputs = inputs.split(os.linesep)
    alterations = dict(a.split(" -> ") for a in alteration_inputs)

    pairs = defaultdict(int)
    for i, j in zip(initial[:-1], initial[1:]):
        pairs[i + j] += 1

    for _ in range(40):
        new_pairs = defaultdict(int)
        for old_pair, num in pairs.items():
            to_inset = alterations[old_pair]
            new_pairs[old_pair[0] + to_inset] += num
            new_pairs[to_inset + old_pair[1]] += num
        pairs = new_pairs

    counts = defaultdict(int)
    for pair, num in pairs.items():
        counts[pair[0]] += num
        counts[pair[1]] += num

    count_values = list(counts.values())

    return (max(count_values) - min(count_values)) // 2 + 1
