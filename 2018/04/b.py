import re

import numpy as np
import pandas as pd


def run(inputs):
    reg = re.compile(r"\[([\d\-:\s]+)\] (.+)")
    s = pd.Series({r[0]: r[1] for r in reg.findall(inputs)})
    s.index = s.index.str.replace("^1518", "2018")
    s.index = pd.to_datetime(s.index, format=r"%Y-%m-%d %H:%M")
    s.sort_index(inplace=True)
    df = s.to_frame("Text")
    df["Guard"] = df.Text.str.extract("#(\d+)").iloc[:, 0].ffill().astype(int)
    df["Minute"] = df.index.minute
    df["Date"] = df.index.date
    df["Asleep"] = df.Text.eq("falls asleep")

    dfp = (
        df[~df.Text.str.startswith("Guard")]
        .pivot_table(index="Minute", columns=["Guard", "Date"], values="Asleep")
        .reindex(range(60))
        .ffill()
        .fillna(False)
        .astype(int)
    )

    return np.product(dfp.sum(axis=1, level=0).unstack().sort_values().index[-1])
