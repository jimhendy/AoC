import re

import pandas as pd


def run(inputs):
    reg = re.compile(r"\[([\d\-:\s]+)\] (.+)")
    s = pd.Series({r[0]: r[1] for r in reg.findall(inputs)})
    s.index = s.index.str.replace("^1518", "2018")
    s.index = pd.to_datetime(s.index, format=r"%Y-%m-%d %H:%M")
    s = s.sort_index()
    df = s.to_frame("Text")
    df["Guard"] = df.Text.str.extract(r"#(\d+)").iloc[:, 0].ffill().astype(int)
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

    total_sleep_minutes = dfp.sum(axis=1, level=0).sum().sort_values()
    sleepiest_guard = total_sleep_minutes.index[-1]

    sleepiest_minute = dfp[sleepiest_guard].sum(axis=1).sort_values().index[-1]

    return sleepiest_guard * sleepiest_minute
