import os
import re

import numpy as np
import pandas as pd


def run(inputs):

    charging_outlet = 0
    inputs = list(map(int, inputs.split(os.linesep)))
    device = max(inputs) + 3

    adapters = pd.Series([charging_outlet, device] + inputs).sort_values()

    diffs = adapters.diff()

    v = diffs.replace({3: np.nan})
    cumsum = v.cumsum().fillna(method="pad")
    reset = -cumsum[v.isnull()].diff().fillna(cumsum)
    one_runs = v.where(v.notnull(), reset).cumsum()
    max_run = int(one_runs.max())  # =4

    s = ",".join(diffs.fillna(3).astype(str).to_list()).replace(".0", "")
    """
    1 = 3,1,3 = 1 = (3,1,3)
    2 = 3,1,1,3 = 2 = (3,1,1,3), (3,2,3)
    3 = 3,1,1,1,3 = 4 = (3,1,2,3), (3,2,1,3), (3,3,3), (3,1,1,1,3)
    4 = 3,1,1,1,1,3 = 7 = (3,1,1,1,1,3), (3,2,1,1,3), (3,3,1,3), (3,1,2,1,3), (3,1,3,3), (3,1,1,2,3), (3,2,2,3)
    """
    total = 1
    for i in range(2, max_run + 1):
        reg_str = "(?=(3," + ",".join(["1"] * i) + ",3))"
        for m in re.findall(reg_str, s):
            total *= {1: 1, 2: 2, 3: 4, 4: 7, 5: 9}[i]

    return total
