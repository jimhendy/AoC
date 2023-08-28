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

    for c in ["cats", "trees"]:
        df = df[df[c].gt(known[c]) | pd.isnull(df[c])]
        pass

    for c in ["pomeranians", "goldfish"]:
        df = df[df[c].lt(known[c]) | pd.isnull(df[c])]
        pass

    for c in df.columns:
        if c in ["cats", "trees", "pomeranians", "goldfish"]:
            continue
        df = df[df[c].eq(known[c]) | pd.isnull(df[c])]
        pass

    assert len(df) == 1

    return df.index[0]
