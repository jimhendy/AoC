import common
import numpy as np
from itertools import permutations

def run(inputs):

    possible_phases = np.arange(5)

    data = {}
    for phases in permutations(possible_phases):
        prev_output = 0
        for p in phases:
            prog = common.optprog(inputs)
            [ prog.analyse_intcode(i) for i in [p, prev_output]]
            prev_output = prog.outputs[-1]
            pass
        data[phases] = prev_output
        pass

    output = sorted(data.items(), key=lambda x : x[1])[-1]

    #print(output)

    return output[1]
