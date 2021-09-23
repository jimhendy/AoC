import pandas as pd
import os

THRESHOLD = 10_000


def run(inputs):

    coords = pd.DataFrame(
        [
            {"x": int(i.split(",")[0]), "y": int(i.split(",")[1])}
            for i in inputs.split(os.linesep)
        ]
    )

    max_coord = coords.max(axis=0)

    space = pd.DataFrame(
        [
            {"x": x, "y": y}
            for x in range(-1, max_coord.x + 2)
            for y in range(-1, max_coord.y + 2)
        ]
    )

    distance_cols = []
    for i in range(len(coords)):
        col = f"Distance_{i}"
        distance_cols.append(col)
        space[col] = abs(space.x - coords.iloc[i].x) + abs(space.y - coords.iloc[i].y)

    space["TotalDistance"] = space[distance_cols].sum(axis=1)

    return space[space.TotalDistance.lt(THRESHOLD)].shape[0]
