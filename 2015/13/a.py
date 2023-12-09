import os
import re
from collections import defaultdict
from itertools import permutations


def run(inputs):
    reg = re.compile(
        r"(\D+) would (\D+) (\d+) happiness units by sitting next to (\D+)\.",
    )

    happiness = defaultdict(lambda: defaultdict(list))

    for match in reg.findall(inputs.replace(os.linesep, "")):
        _sign = +1 if match[1] == "gain" else -1
        happiness[match[0]][match[3]] = _sign * int(match[2])

    max_happiness = 0
    for p in permutations(happiness.keys()):
        this_happiness = 0
        for p_0, p_1 in zip(p[:-1], p[1:]):
            this_happiness += happiness[p_0][p_1]
            this_happiness += happiness[p_1][p_0]
        # Edge people
        this_happiness += happiness[p[0]][p[-1]]
        this_happiness += happiness[p[-1]][p[0]]

        if this_happiness > max_happiness:
            max_happiness = this_happiness

    return max_happiness
