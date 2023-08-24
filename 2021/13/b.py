import os

import numpy as np
import pandas as pd


def fold(points, value, axis):
    mask = points[:, axis] > value
    points[mask, axis] = 2 * value - points[mask, axis]


def run(inputs):

    points = []
    folds = []
    for line in inputs.split(os.linesep):
        if "," in line:
            points.append(line.split(","))
        elif "fold" in line:
            folds.append(line.split()[-1])
    points = np.array(points).astype(int)

    for f in folds:
        value = int(f.split("=")[1])
        fold(points, value, int(f.startswith("y")))

    df = (
        pd.DataFrame(points, columns=["x", "y"])
        .assign(v="#")
        .pivot_table(index="y", columns="x", values="v", aggfunc="first")
        .fillna("")
    )

    print(df)

    raise NotImplementedError("Read the above letters, do not automatically submit")
