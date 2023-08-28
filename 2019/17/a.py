import os

import intcode
import numpy as np


def run(inputs):
    prog = intcode.Intcode(inputs)
    prog.analyse_intcode()

    data = np.array(list(map(chr, prog.outputs)))[:-1]

    data = data.reshape(-1, int(np.argwhere(data == os.linesep)[0] + 1))
    data = np.delete(data, -1, axis=1)

    positions = []
    for y in range(1, data.shape[0] - 1):
        for x in range(1, data.shape[1] - 1):
            if data[y][x] == "#":
                others = [
                    data[y - 1][x],
                    data[y + 1][x],
                    data[y][x - 1],
                    data[y][x + 1],
                ]
                if all(i == "#" for i in others):
                    positions.append(x * y)
                    pass
                pass
            pass
        pass
    return sum(positions)
