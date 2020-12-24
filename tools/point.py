import itertools


class Point:
    def __init__(self, *x):
        self.x = x
        self.steps = {}  # To be set in sub-class

    def tup(self):
        return tuple(self.x)

    def __repr__(self):
        return f"({','.join(map(str, self.x))})"

    def __eq__(self, other):
        return all(
            [s == o for s, o in itertools.zip_longest(self.x, other.x, fillvalue=0)]
        )

    def __add__(self, other):
        return type(self)(
            *[s + o for s, o in itertools.zip_longest(self.x, other.x, fillvalue=0)]
        )

    def __sub__(self, other):
        return type(self)(
            *[s - o for s, o in itertools.zip_longest(self.x, other.x, fillvalue=0)]
        )

    def copy(self):
        return self.__copy__()

    def __abs__(self):
        return sum([abs(i) for i in self.x])

    def __copy__(self):
        return type(self)(*self.x)

    def __iadd__(self, other):
        self.x = (self + other).x
        return self

    def __isub__(self, other):
        self.x = (self - other).x
        return self

    def __hash__(self):
        return hash(self.x)

    def neighbour(self, direction):
        return self + self.steps[direction]

    def all_neighbours(self):
        if not len(self.steps):
            raise RuntimeError(
                'Trying to find neighbours for a Point baseclass with no "steps" attribute'
            )
        for s in self.steps.values():
            yield self + s


class Point2D(Point):
    steps = {
        "down": Point(0, 1),
        "up": Point(0, -1),
        "left": Point(-1, 0),
        "right": Point(1, 0),
        "up-left": Point(-1, -1),
        "up-right": Point(1, -1),
        "down-left": Point(-1, 1),
        "down-right": Point(1, 1),
    }  # diagonals involve dash to differentiate

    def __init__(self, x, y):
        super().__init__(x, y)
        self.steps = Point2D.steps

    def nb4(self):
        for k, v in self.steps.items():
            if "-" in k:
                continue
            yield self + v

    def nb8(self):
        yield from self.all_neighbours()


class PointyTop2DHexPoint(Point):
    steps = {
        "nw": Point(-1, 0, +1),
        "ne": Point(0, +1, +1),
        "e": Point(+1, +1, 0),
        "w": Point(-1, -1, 0),
        "se": Point(+1, 0, -1),
        "sw": Point(0, -1, -1),
    }

    def __init__(self, x, y, z=0):
        super().__init__(x, y, z)
        self.steps = PointyTop2DHexPoint.steps


class FlatTop2DHexPoint(Point):
    steps = {
        "n": Point(0, +1, -1),
        "ne": Point(+1, 0, -1),
        "se": Point(+1, -1, 0),
        "s": Point(0, -1, +1),
        "sw": Point(-1, 0, +1),
        "nw": Point(-1, +1, 0),
    }

    def __init__(self, x, y, z=0):
        super().__init__(x, y, z)
        self.steps = FlatTop2DHexPoint.steps
