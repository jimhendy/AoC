import os

import numpy as np
from tile import Tile


def run(inputs):
    tiles = [Tile(i) for i in inputs.split(os.linesep * 2)]

    for ti in tiles:
        for _, ei in ti.nominal_edges():
            for tj in tiles:
                if tj == ti:
                    continue
                for _, ej in tj.edges():
                    if ei == ej:
                        ti.matches.append(tj)

    sorted_tiles = sorted(tiles, key=lambda x: len(x.matches))

    return np.prod([t.id_num for t in sorted_tiles[:4]])
