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
                Point3D(*map(int, start.split(","))), Point3D(*map(int, end.split(",")))
            )
        )

    return len(bricks)
