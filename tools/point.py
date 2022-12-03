import itertools
from typing import Iterable, Optional, Tuple, Union


class Point:
    def __init__(self, *values):
        self.values = values
        self.steps = {}  # To be set in sub-class

    @property
    def x(self):
        return self.values

    def tup(self):
        return tuple(self.values)

    def __repr__(self):
        return f"({','.join(map(str, self.values))})"

    def __eq__(self, other):
        return all(
            [
                s == o
                for s, o in itertools.zip_longest(
                    self.values, other.values, fillvalue=0
                )
            ]
        )

    def __add__(self, other):
        return type(self)(
            *[
                s + o
                for s, o in itertools.zip_longest(
                    self.values, other.values, fillvalue=0
                )
            ]
        )

    def __sub__(self, other):
        return type(self)(
            *[
                s - o
                for s, o in itertools.zip_longest(
                    self.values, other.values, fillvalue=0
                )
            ]
        )

    def copy(self):
        return self.__copy__()

    def __abs__(self):
        return sum([abs(i) for i in self.values])

    def __copy__(self):
        return type(self)(*self.values)

    def __iadd__(self, other):
        self.values = (self + other).values
        return self

    def __isub__(self, other):
        self.values = (self - other).values
        return self

    def __hash__(self):
        return hash(self.values)

    def __len__(self):
        return len(self.values)

    def neighbour(self, direction):
        return self + self.steps[direction]

    def all_neighbours(
        self, grid_size: Optional[Union[int, Tuple[int, int]]] = None
    ) -> Iterable["Point"]:
        if not len(self.steps):
            raise RuntimeError(
                'Trying to find neighbours for a Point baseclass with no "steps" attribute'
            )

        if isinstance(grid_size, int):
            grid_size = [grid_size] * len(self)

        if grid_size is not None:
            grid_size = tuple(grid_size)
            assert len(grid_size) == len(
                self
            ), f"grid_size must be an int or a {len(self)}-tuple of ints"
            assert all([i > 0 for i in grid_size]), f"grid_size must be positive"

        for s in self.steps.values():
            neighbour = self + s

            if grid_size is not None:

                if any([v < 0 for v in neighbour.values]):
                    continue

                if any([v >= g for v, g in zip(neighbour.values, grid_size)]):
                    continue

            yield neighbour


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

    @property
    def x(self):
        return self.values[0]

    @property
    def y(self):
        return self.values[1]

    def __init__(self, x, y):
        super().__init__(x, y)
        self.steps = Point2D.steps

    def nb4(
        self, grid_size: Optional[Union[int, Tuple[int, int]]] = None
    ) -> Iterable["Point2D"]:
        """
        Generator of the 4 nearest neighbours to this point.
        No diagonals are included.

        :param grid_size: (Optional) size of grid we are considering, will not return \
            points with negatiev co-ordinates or values beyond the end of the grid.
            Can either be and ``int`` for a square grid or a ``tuple`` of 2 ``int``s.
        """
        if isinstance(grid_size, int):
            grid_size = (grid_size, grid_size)

        if grid_size is not None:
            grid_size = tuple(grid_size)
            assert len(grid_size) == 2, f"grid_size must be an int or a 2-tuple of ints"
            assert grid_size[0] > 0 and grid_size[1] > 0, f"grid_size must be positive"

        for k, v in self.steps.items():
            if "-" in k:
                continue
            new_x = self.x + v.values[0]
            new_y = self.y + v.values[1]
            if grid_size is not None and (
                not (0 <= new_x < grid_size[0]) or not (0 <= new_y < grid_size[1])
            ):
                continue

            neighbour = Point2D(new_x, new_y)

            yield neighbour

    def nb8(
        self, grid_size: Optional[Union[int, Tuple[int, int]]] = None
    ) -> Iterable["Point2D"]:
        """
        Generator of the 8 nearest neighbours to this point.
        Diagonals are included.

        :param grid_size: (Optional) size of grid we are considering, will not return \
            points with negatiev co-ordinates or values beyond the end of the grid.
            Can either be and ``int`` for a square grid or a ``tuple`` of 2 ``int``s.
        """
        yield from self.all_neighbours(grid_size=grid_size)


class PointyTop2DHexPoint(Point):
    # See https://www.redblobgames.com/grids/hexagons/
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
