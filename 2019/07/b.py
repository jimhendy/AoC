from itertools import permutations

import common
import numpy as np


def run(inputs):
    possible_phases = np.arange(5, 10)

    data = {}
    for phases in permutations(possible_phases):
        prev_output = 0
        amps = [common.optprog(inputs) for p in phases]

        # Run the first iteration using the phases
        [a.analyse_intcode(p) for a, p in zip(amps, phases)]

        while not all(a.complete for a in amps):
            for a in amps:
                a.analyse_intcode(prev_output)
                prev_output = a.outputs[-1]
        data[phases] = prev_output

    output = sorted(data.items(), key=lambda x: x[1])[-1]

    return output[1]
