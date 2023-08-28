from collections import Counter

import common
from intcode import optprog


def run(inputs):
    prog = optprog(inputs)
    prog.analyse_intcode()
    counts = Counter(prog.outputs[2::3])
    return counts[common.Tile.BLOCK.value]
