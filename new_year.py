import datetime
import pathlib


def new_year(year: int) -> None:
    year_dir = pathlib.Path(str(year))
    year_dir.mkdir(exist_ok=True)
    for day in range(1, 26):
        day_dir = year_dir / f"{day:02}"
        day_dir.mkdir(exist_ok=True)
        for part in "ab":
            filename = day_dir / f"{part}.py"
            if filename.exists():
                continue
            filename.touch(exist_ok=True)
            with filename.open("w") as f:
                f.write("def run(input: str) -> int:\n")
                f.write("    return 0\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--year",
        type=int,
        help="Year to create folder structure for",
        default=datetime.datetime.now(tz=datetime.UTC).year,
    )
    args = parser.parse_args()

    new_year(args.year)
