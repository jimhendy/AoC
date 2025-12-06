import re

from tools.point import Point3D


def _parse_inputs(inputs: str) -> list[tuple[Point3D, Point3D]]:
    """
    Extract the points from the input string.

    Input string is in the format:
    x1,y1,z1~x2,y2,z2

    Each value is an integer.
    The first point (x1, y1, z1) is actually the top right corner of the box so
    we subtract 1 from each value to get the bottom left corner.
    """
    regex = re.compile(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)")
    return [
        (
            Point3D(int(match.group(1)), int(match.group(2)), int(match.group(3))),
            Point3D(int(match.group(4)), int(match.group(5)), int(match.group(6))),
        )
        for match in regex.finditer(inputs)
    ]


def run(inputs: str) -> int:
    points = _parse_inputs(inputs)


from dataclasses import dataclass

from tools.point import Point3D


@dataclass
class Brick:
    start: Point3D
    end: Point3D


def run(inputs: str) -> int:
    bricks = []
    for line in inputs.splitlines():
        start, end = line.split("~")
        bricks.append(
            Brick(
                Point3D(*map(int, start.split(","))),
                Point3D(*map(int, end.split(","))),
            ),
        )

    return len(bricks)
