import pathlib
import subprocess


def new_year(year: int) -> None:
    year_dir = pathlib.Path(str(year))
    year_dir.mkdir(exist_ok=True)
    for day in range(1, 26):
        day_dir = year_dir / f"{day:02}"
        day_dir.mkdir(exist_ok=True)
        for part in "ab":
            filename = day_dir / f"{part}.py"
            subprocess.call(f"touch {filename!s}", shell=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int, help="Year to create folder structure for")
    args = parser.parse_args()

    new_year(args.year)
