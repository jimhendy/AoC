from point import Point
import os

DIRECTIONS = {
    "E": Point(+1, 0),
    "W": Point(-1, 0),
    "N": Point(0, -1),
    "S": Point(0, +1),
}

LEFT = {"E": "N", "S": "E", "W": "S", "N": "W"}

RIGHT = {"E": "S", "S": "W", "W": "N", "N": "E"}


def run(inputs):

    heading = "E"
    pos = Point(0, 0)

    for line in inputs.split(os.linesep):
        code = line[0]
        if code in "NSEW":
            steps = int(line[1:])
            for _ in range(steps):
                pos += DIRECTIONS[code]
        elif code == "F":
            steps = int(line[1:])
            for _ in range(steps):
                pos += DIRECTIONS[heading]
        elif code in "RL":
            turn = RIGHT if code == "R" else LEFT
            steps = int(line[1:]) // 90
            for _ in range(steps):
                heading = turn[heading]
    return abs(pos.x) + abs(pos.y)
