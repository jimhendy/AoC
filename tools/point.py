import itertools
from collections.abc import Iterable
from contextlib import contextmanager
from typing import ClassVar, Self

import numpy as np
from numba import njit

from tools.errors import PointError

DTYPE = np.int64


class Point:
    __slots__ = ("values",)

    def __init__(self, *values: list[float]) -> None:
        self.values = np.array(values, dtype=DTYPE)

    @classmethod
    def from_iterable(cls, values: Iterable[float]) -> Self:
        new = cls()
        new.values = np.array(values)
        return new

    @staticmethod
    @njit(
        "int64[:](int64[:], int64[:], int64)",
        cache=True,
    )
    def _add_values(
        a: np.ndarray[DTYPE],
        b: np.ndarray[DTYPE],
        fill_value: DTYPE = 0,
    ) -> np.ndarray[DTYPE]:
        a_len = a.shape[0]
        b_len = b.shape[0]

        result = np.full(max(a_len, b_len), fill_value=fill_value, dtype=DTYPE)
        result[:a_len] += a
        result[:b_len] += b
        return result

    @property
    def steps(self) -> dict[str, Self]:
        return {}  # To be set in sub-class

    def step(self, direction: str) -> Self:
        return self + self.steps[direction]

    @property
    def x(self):
        return self.values

    def tup(self) -> tuple[float, ...]:
        return tuple(self.values)

    def __repr__(self) -> str:
        return f"({','.join(map(str, self.values))})"

    def __eq__(self, other: Self | Iterable[float]) -> bool:
        if isinstance(other, Point):
            other = other.values  # noqa: PD011
        return all(
            s == o for s, o in itertools.zip_longest(self.values, other, fillvalue=0)
        )

    def __add__(self, other: Self | float) -> Self:
        if isinstance(other, Point):
            new_values = self._add_values(self.values, other.values, 0)
        else:
            new_values = self.values + other
        return self.from_iterable(new_values)

    def __neg__(self) -> Self:
        return self * -1

    def __sub__(self, other: Self | float) -> Self:
        return self + (-other)

    def __mul__(self, other: float) -> Self:
        return self.from_iterable(other * self.values)

    def __truediv__(self, other: float) -> Self:
        return self * (1 / other)

    def __floordiv__(self, other: float) -> Self:
        true_div = self / other
        return self.from_iterable(np.trunc(true_div.values))

    def copy(self) -> Self:
        return self.__copy__()

    def __abs__(self, order: int = 1) -> float:
        return np.linalg.norm(self.values, ord=order)

    def __copy__(self) -> Self:
        return self.from_iterable(self.values)

    def __iadd__(self, other: Self | float) -> Self:
        if isinstance(other, Point):
            self.values += other.values  # noqa: PD011
        else:
            self.values += other
        return self

    def __isub__(self, other: Self | float) -> Self:
        return self.__iadd__(-other)

    def __hash__(self):
        return hash(self.tup())

    def __len__(self) -> int:
        return len(self.values)

    def neighbour(self, direction: str) -> Self:
        return self + self.steps[direction]

    def distance_to(self, other: Self, order: int = 1) -> float:
        return np.linalg.norm(self.values - other.values, ord=order)  # noqa: PD011

    def __iter__(self):
        yield from self.values

    @contextmanager
    def _temporary_steps(self, new_steps):
        original_steps = self.steps
        self.steps = new_steps
        try:
            yield
        finally:
            self.steps = original_steps

    def all_neighbours(
        self,
        grid_size: int | tuple[int, ...] | None = None,
    ) -> Iterable[Self]:
        """
        Generates all the neighboring points of the current point.

        Args:
        ----
            grid_size (int or tuple[int, ...] or None): The size of the grid or None
                    if there is no grid. Negative values are allowed.
                If an int is provided, it is assumed that the grid is a square grid
                    with equal sides. No negative values allowed.
                If a tuple is provided, it should contain the size of each dimension
                    of the grid. No negative values allowed.


        Returns:
        -------
            Iterable[Point]: A generator that yields all the neighboring points.


        Raises:
        ------
            PointError: If the current point does not have a "steps" attribute.
            PointError: If the grid_size is not compatible with the dimensions of the
                point.
            PointError: If any dimension of the grid_size is not positive.

        """
        # Check if the current point has a "steps" attribute
        if not len(self.steps):
            msg = (
                "Trying to find neighbours for a Point baseclass with no "
                '"steps" attribute'
            )
            raise RuntimeError(msg)

        # Convert grid_size to a tuple if it is an int
        if isinstance(grid_size, int):
            grid_size = [grid_size] * len(self)

        # Perform grid_size validation
        if grid_size is not None:
            grid_size = tuple(grid_size)
            if len(grid_size) != len(self):
                error = f"grid_size must be an int or a {len(self)}-tuple of ints"
                raise PointError(error)
            if not all(i >= 0 for i in grid_size):
                error = "Grid_size must be positive"
                raise PointError(error)
            if any(point >= grid for point, grid in zip(self, grid_size, strict=True)):
                error = f"Initial point is outside the grid. {grid_size=}, {self=}"
                raise PointError(error)

        # Generate all the neighboring points
        for s in self.steps.values():
            neighbour = self + s

            if grid_size is not None:
                if any(v < 0 for v in neighbour.values):  # noqa: PD011
                    continue

                if any(
                    v >= g for v, g in zip(neighbour.values, grid_size, strict=True)
                ):
                    continue

            yield neighbour


class Point2D(Point):
    steps: ClassVar[dict[str, Point]] = {
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

    def __init__(self, x: float = 0, y: float = 0) -> None:
        super().__init__(x, y)

    def nb4(
        self,
        grid_size: int | tuple[int, int] | None = None,
    ) -> Iterable["Point2D"]:
        """
        Generator of the 4 nearest neighbours to this point.
        No diagonals are included.

        :param grid_size: (Optional) size of grid we are considering, will not return \
            points with negatiev co-ordinates or values beyond the end of the grid.
            Can either be and ``int`` for a square grid or a ``tuple`` of 2 ``int``s.
        """
        non_diagonal_steps = {k: v for k, v in self.steps.items() if "-" not in k}
        with self._temporary_steps(non_diagonal_steps):
            yield from self.all_neighbours(grid_size=grid_size)

    def nb8(
        self,
        grid_size: int | tuple[int, int] | None = None,
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
    steps: ClassVar[dict[str, Point]] = {
        "nw": Point(-1, 0, +1),
        "ne": Point(0, +1, +1),
        "e": Point(+1, +1, 0),
        "w": Point(-1, -1, 0),
        "se": Point(+1, 0, -1),
        "sw": Point(0, -1, -1),
    }

    def __init__(self, x, y, z=0) -> None:
        super().__init__(x, y, z)


class FlatTop2DHexPoint(Point):
    steps: ClassVar[dict[str, Point]] = {
        "n": Point(0, +1, -1),
        "ne": Point(+1, 0, -1),
        "se": Point(+1, -1, 0),
        "s": Point(0, -1, +1),
        "sw": Point(-1, 0, +1),
        "nw": Point(-1, +1, 0),
    }

    def __init__(self, x, y, z=0) -> None:
        super().__init__(x, y, z)


class Point3D(Point):
    steps: ClassVar[dict[str, Point]] = {
        "down": Point(0, 0, 1),
        "up": Point(0, 0, -1),
        "left": Point(-1, 0, 0),
        "right": Point(1, 0, 0),
        "in": Point(0, 1, 0),
        "out": Point(0, -1, 0),
        # In plane diagonals
        "down-left": Point(-1, 0, 1),
        "down-right": Point(1, 0, 1),
        "up-left": Point(-1, 0, -1),
        "up-right": Point(1, 0, -1),
        # Out of plane diagonals
        "down-in": Point(0, 1, 1),
        "down-out": Point(0, -1, 1),
        "up-in": Point(0, 1, -1),
        "up-out": Point(0, -1, -1),
        "left-in": Point(-1, 1, 0),
        "left-out": Point(-1, -1, 0),
        "right-in": Point(1, 1, 0),
        "right-out": Point(1, -1, 0),
        # Double diagonals
        "down-left-in": Point(-1, 1, 1),
        "down-left-out": Point(-1, -1, 1),
        "down-right-in": Point(1, 1, 1),
        "down-right-out": Point(1, -1, 1),
        "up-left-in": Point(-1, 1, -1),
        "up-left-out": Point(-1, -1, -1),
        "up-right-in": Point(1, 1, -1),
        "up-right-out": Point(1, -1, -1),
    }

    @property
    def x(self):
        return self.values[0]

    @property
    def y(self):
        return self.values[1]

    @property
    def z(self):
        return self.values[2]

    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        super().__init__(x, y, z)

    def nb6(
        self,
        grid_size: int | tuple[int, int] | None = None,
    ) -> Iterable["Point3D"]:
        """
        Generator of the 6 nearest neighbours to this point.
        No diagonals are included.
        """
        non_diagonal_steps = {k: v for k, v in self.steps.items() if "-" not in k}
        with self._temporary_steps(non_diagonal_steps):
            yield from self.all_neighbours(grid_size=grid_size)
