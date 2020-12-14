import os
import re

import pandas as pd

def run(inputs):
    reg = re.compile(r"([\-\d]+)")
    bots = pd.DataFrame(
        [reg.findall(line) for line in inputs.split(os.linesep)], columns=list("xyzr")
    ).astype(int)

    scale = bots.r.min() // 2
    mins = {o: bots[o].div(scale).astype(int).min() for o in list("xyz")}
    maxs = {o: bots[o].div(scale).astype(int).max() for o in list("xyz")}

    while scale >= 1:
        scaled_bots = bots.div(scale).astype(int)
        data = []
        for x in range(mins["x"], maxs["x"] + 1):
            for y in range(mins["y"], maxs["y"] + 1):
                for z in range(mins["z"], maxs["z"] + 1):
                    for b in scaled_bots.itertuples():
                        overlap = abs(b.x-x) + abs(b.y-y) + abs(b.z-z) <= b.r
                        data.append({"x": x, "y": y, "z": z, "overlap": int(overlap)})
        df = pd.DataFrame(data).groupby(["x", "y", "z"]).overlap.sum()
        max_overlaps = df[df.eq(df.max())]
        max_overlaps = max_overlaps.to_frame("overlaps").reset_index(drop=False)

        if scale == 1:
            break

        new_scale = scale // 2
        scale_change = scale / new_scale
        mins = {i: int((max_overlaps[i].min() - 1) * scale_change) for i in list("xyz")}
        maxs = {i: int((max_overlaps[i].max() + 1) * scale_change) for i in list("xyz")}

        scale = new_scale

    max_overlaps["dist"] = max_overlaps[list("xyz")].abs().sum(axis=1)

    return max_overlaps[max_overlaps.dist.eq(max_overlaps.dist.min())].iloc[0].dist
