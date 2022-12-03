import numpy as np
import pandas as pd
from status import Status


def run(inputs):

    status = Status(inputs)

    size = 1e7
    data = {}
    for depth, layer in status.layers.items():
        cycle = list(range(layer.range))
        cycle += cycle[-2:0:-1]
        cycle = np.roll(np.array(cycle), -depth)
        n_repeats = int(np.ceil(size / len(cycle)))
        data[depth] = np.tile(cycle, n_repeats)[: int(size)]
    df = pd.DataFrame(data)
    return df.ne(0).all(axis=1).replace(False, np.nan).dropna().index[0]
