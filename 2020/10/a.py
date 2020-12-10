import os
import pandas as pd


def run(inputs):

    charging_outlet = 0
    inputs = list(map(int, inputs.split(os.linesep)))
    device = max(inputs) + 3

    adapters = pd.Series([charging_outlet, device] + inputs).sort_values()

    diffs = adapters.diff().value_counts()

    print(diffs)

    return diffs.loc[1] * diffs.loc[3]
