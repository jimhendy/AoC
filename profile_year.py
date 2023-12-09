import argparse
import os
import subprocess
import time
from pathlib import Path

import pandas as pd
from loguru import logger

# Time each day & part for a given year's code and print a table of the slowest
# parts for optimisation

parser = argparse.ArgumentParser()
parser.add_argument("--year", type=int, help="Year to profile", default=-1)
args = parser.parse_args()


def run_part(part_file):
    logger.info(f"Running {part_file}")
    cmd = f"python main.py {part_file}"
    start = time.time()
    subprocess.call(cmd, shell=True)  # noqa: S602
    return time.time() - start


def profile_year(year: Path):
    if not year.is_dir():
        logger.error(f"Year {year} does not exist")
        return
    parts = sorted(year.glob("??/[a|b].py"))
    data = {f: run_part(f) for f in parts}
    df = (
        pd.Series(data)
        .to_frame("Time")
        .round(2)
        .rename_axis("FName", axis=0)
        .reset_index(drop=False)
    )
    total = df.Time.sum()
    df["Part"] = df.FName.str.split(os.path.sep).str[2].str.split(".").str[0]
    df["Day"] = df.FName.str.split(os.path.sep).str[1].astype(int)
    df = df.pivot_table(index="Day", columns="Part", values="Time")
    df["Combined"] = df.sum(axis=1)
    logger.info(df)
    logger.info("=" * 30)
    logger.info(df.sort_values("Combined", ascending=False))
    logger.info("=" * 30)
    logger.info(f"Total: {total} s")


if __name__ == "__main__":
    if args.year != -1:
        profile_year(args.year)
    else:
        years = sorted(
            [directory.name for directory in Path().glob("20??") if directory.is_dir()],
        )
        logger.info(years)
        [profile_year(Path(d)) for d in years]
