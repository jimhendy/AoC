import re
import os
import pandas as pd
from point import Point
from collections import defaultdict
import sys

sys.setrecursionlimit(10_000)


def find_clay(inputs):
    df = pd.DataFrame(
        re.findall(r"(x|y)=([\-\d]+), (?:x|y)=([\-\d]+)\.\.([\-\d]+)", inputs),
        columns=["Direction", "Value", "Start", "End"],
    ).astype({"Value": int, "Start": int, "End": int})

    return {
        Point(row.Value, i) if row.Direction == "x" else Point(i, row.Value)
        for row in df.itertuples()
        for i in range(row.Start, row.End + 1)
    }


def is_static(loc, grid, direction=None):
    grid['falling'].add(loc)
    below, left, right = (loc.neighbour(d) for d in ('down','left','right'))

    if not below in grid['clay']:
        if below not in grid['falling'] and 1 <= below.y <= MAX_Y:
            # Don't yet know what this loc is
            is_static(below, grid)
        if below not in grid['static']:
            # Either already evaluated or outside area of concern
            return False

    # Is the loc to the left(/right) static?
    # Yes if
    # * Clay
    # * or not yet evaulated and is_static (only going left(/right))
    left_static = left in grid['clay'] or (left not in grid['falling'] and is_static(left, grid, direction='left'))
    right_static = right in grid['clay'] or (right not in grid['falling'] and is_static(right, grid, direction='right'))

    if direction == None and left_static and right_static:
        # If going down and letf & right are static
        grid['static'].add(loc)

        while left in grid['falling']:
            grid['static'].add(left)
            left = left.neighbour('left')

        while right in grid['falling']:
            grid['static'].add(right)
            right = right.neighbour('right')

    # is_static = everything in either direction is also static
    return direction == 'left' and (left_static or left in grid['clay']) or direction == 'right' and (right_static or right in grid['clay'])



def display(grid):
    y = set([p.y for p in grid['clay'] | grid['falling'] | grid['static']])
    x = set([p.x for p in grid['clay'] | grid['falling'] | grid['static']])
    df = pd.DataFrame(
        ".",
        index=list(range(min(y) - 1, max(y) + 2)),
        columns=list(range(min(x) - 1, max(x) + 2)),
    )
    for p in grid['clay']:
        df.loc[p.y, p.x] = "#"
    for p in grid['falling']:
        df.loc[p.y, p.x] = "|"
    for p in grid['static']:
        df.loc[p.y, p.x] = "~"
    print(os.linesep.join(["".join(v) for v in df.values]))


def run(inputs):
    global MAX_Y
    
    spring = Point(500, 0)
    grid = defaultdict(set)
    grid['clay'] = find_clay(inputs)

    ys = [p.y for p in grid['clay']]
    MIN_Y, MAX_Y = min(ys), max(ys)

    is_static(spring.neighbour('down'), grid)
    #display(grid)

    return len([p for p in grid['static'] if MIN_Y <= p.y <= MAX_Y])
