from point import Point
import os

DIRECTIONS = {
    "E": Point(+1, 0),
    "W": Point(-1, 0),
    "N": Point(0, -1),
    "S": Point(0, +1),
}


def right(current):
    return Point(-current.y, current.x)


def left(current):
    return Point(current.y, -current.x)


def run(inputs):

    waypoint = Point(10, -1)  # Always relative to ship
    ship = Point(0, 0)

    for line in inputs.split(os.linesep):
        code = line[0]
        if code in "NSEW":
            steps = int(line[1:])
            for _ in range(steps):
                waypoint += DIRECTIONS[code]
        elif code == "F":
            steps = int(line[1:])
            for _ in range(steps):
                ship += waypoint
        elif code in "RL":
            turn = right if code == "R" else left
            steps = int(line[1:]) // 90
            for _ in range(steps):
                waypoint = turn(waypoint)

    return abs(ship.x) + abs(ship.y)
