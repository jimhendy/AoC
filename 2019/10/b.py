import common
import numpy as np
import pandas as pd


def run(inputs):

    data = common.in_to_array(inputs)

    visible = common.num_visible(data)
    station_coords = visible.index[-1]

    position = np.array([station_coords])

    angle = common._get_angle(data, position)
    r = common._get_distance(data, position)

    df = pd.DataFrame(
        {"R": r, "Phi": angle, "X": data[:, 0], "Y": data[:, 1]}
    ).sort_values("R")
    # Remove the station itself
    df = df[df.R != 0]

    df["R_rank"] = df.groupby("Phi").R.rank()
    df.sort_values(["R_rank", "Phi"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    pos_i = 200 - 1
    return df.iloc[pos_i].X * 100 + df.Y.iloc[pos_i]
