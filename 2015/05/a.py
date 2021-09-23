import os
import numpy as np
import pandas as pd


def run(inputs):

    df = pd.DataFrame([list(i) for i in inputs.split(os.linesep)])
    s = pd.Series(inputs.split(os.linesep))

    vowels = list("aeiou")
    bad_strings = ["ab", "cd", "pq", "xy"]

    vowels_mask = df.isin(vowels).sum(axis=1).gt(2)
    repeats_mask = df.applymap(ord).diff(axis=1).eq(0).any(axis=1)
    bad_mask = s.apply(lambda x: sum([i in x for i in bad_strings]) == 0)

    return len(df[vowels_mask & repeats_mask & bad_mask])
