import pandas as pd
import re
import os


def run(inputs):
    reg = re.compile(r"([\-\d]+)")
    df = pd.DataFrame(
        [reg.findall(line) for line in inputs.split(os.linesep)], columns=list("xyzr")
    ).astype(int)
    max_r = df.loc[df.r.idxmax()]

    for o in list("xyz"):
        df[f"d{o}"] = df[o] - max_r[o]

    df["dist"] = df[["dx", "dy", "dz"]].abs().sum(axis=1)

    return len(df[df.dist.le(max_r.r)])
