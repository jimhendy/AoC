import os
from collections import Counter, deque


def step(q, alterations):
    len_before_step = len(q)
    for _ in range(len_before_step - 1):
        starting_pair = q[0] + q[1]
        to_insert = alterations.get(starting_pair)

        if to_insert:
            q.rotate(-1)
            q.appendleft(to_insert)

        q.rotate(-1)
    q.rotate(-1)


def run(inputs):
    initial, _, *alteration_inputs = inputs.split(os.linesep)
    alterations = dict(a.split(" -> ") for a in alteration_inputs)
    q = deque(list(initial))

    [step(q, alterations) for _ in range(10)]

    counts = Counter(q)
    count_values = list(counts.values())

    return max(count_values) - min(count_values)
