import os
import pandas as pd


def run(inputs):

    counts = {2: 0, 3: 0}

    for box in inputs.split(os.linesep):
        letters = pd.Series(list(box))
        box_counts = letters.value_counts()
        for k, v in counts.items():
            if k in box_counts.values:
                counts[k] = v + 1

    return counts[2] * counts[3]
