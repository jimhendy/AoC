from dataclasses import dataclass, field
from loguru import logger
from itertools import combinations
import math


MIN = 200_000_000_000_000
MAX = 400_000_000_000_000


@dataclass
class Point:
    x: float
    y: float

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __abs__(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self) -> "Point":
        size = abs(self)
        return Point(self.x / size, self.y / size)

    def __eq__(self, other: "Point") -> bool:
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)


@dataclass
class Particle:
    position: Point
    velocity: Point

    gradient: float = field(init=False)
    intercept: float = field(init=False)

    def __post_init__(self):
        self.gradient = self.velocity.y / self.velocity.x
        self.intercept = self.position.y - self.gradient * self.position.x

    @staticmethod
    def split_2d(string: str) -> Point:
        values = map(int, string.split(","))
        return Point(next(values), next(values))

    @classmethod
    def from_string(cls, string: str):
        parts = string.split("@")
        pos = cls.split_2d(parts[0])
        vel = cls.split_2d(parts[1])
        return cls(position=pos, velocity=vel)

    def _will_hit_point(self, point: Point) -> bool:
        """
        Test if this particle will go in the correct direction to hit the given point

        E.g.
        >>> p = Particle.from_string("1,2,3@1,1,1")

        >>> p._will_hit_point(Point(1, 2))
        True

        >>> p._will_hit_point(Point(1, 3))
        False

        >>> p._will_hit_point(Point(2, 3))
        True

        >>> p._will_hit_point(Point(0, 1))
        False # As it is going in the wrong direction
        """
        if point == self.position:
            return True
        result = (point - self.position).normalize() == self.velocity.normalize()
        # logger.debug(f"Will hit point {point}: {result}")
        return result

    def intercepts(self, other: "Particle") -> bool:
        if self.gradient == other.gradient:
            return False

        x = (other.intercept - self.intercept) / (self.gradient - other.gradient)
        if x < MIN or x > MAX:
            # logger.debug(f"X out of range: {x} for {self} and {other}")
            return False

        y = self.gradient * x + self.intercept
        if y < MIN or y > MAX:
            # logger.debug(f"Y out of range: {y} for {self} and {other}")
            return False
        # logger.debug(f"Intercept at ({x}, {y}) for {self} and {other}")
        intercept = Point(x, y)

        # logger.debug(f"Intercept at {intercept}")
        if not self._will_hit_point(intercept):
            # logger.debug(f"Intercept not on line (self) for {self} and {other}")
            return False

        if not other._will_hit_point(intercept):
            # logger.debug(f"Intercept not on line (other) for {self} and {other}")
            return False

        # logger.debug(f"Intercept at {intercept} for {self} and {other}")
        return True


def run(inputs: str) -> int:
    particles = [Particle.from_string(line) for line in inputs.splitlines()]

    num_intercepts = 0
    for p1, p2 in combinations(particles, 2):
        if p1.intercepts(p2):
            num_intercepts += 1

    return num_intercepts
