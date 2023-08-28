import os
import re

import pandas as pd


def run(inputs):
    stuff_reg = re.compile(r"(\w+)\: (-?\d+)")
    sue_reg = re.compile(r"Sue (\d+)\:")

    sues = {}
    for i in inputs.split(os.linesep):
        stuff = stuff_reg.findall(i)
        sues[int(sue_reg.findall(i)[0])] = {i[0]: int(i[1]) for i in stuff}
        pass

    df = pd.DataFrame(sues).T

    known = pd.Series(
        {
            "children": 3,
            "cats": 7,
            "samoyeds": 2,
            "pomeranians": 3,
            "akitas": 0,
            "vizslas": 0,
            "goldfish": 5,
            "trees": 3,
            "cars": 2,
            "perfumes": 1,
        },
    )

    sue = df.sub(known).abs().sum(axis=1).eq(0).replace(False, pd.np.nan).dropna().index

    assert len(sue) == 1

    return sue[0]
