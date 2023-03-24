import uuid
from dataclasses import dataclass, field
from typing import Dict, Iterable, List

from tools.a_star import State, a_star
from tools.point import Point2D

DIRECTIONS = {">": "right", "<": "left", "^": "up", "v": "down"}

WALLS: set[Point2D] = set()
GRID_HEIGHT: int = -1  # Includes walls
GRID_WIDTH: int = -1
DESTINATION: Point2D = Point2D(x=-1, y=-1)


@dataclass
class Blizzard:
    location: Point2D
    direction: str

    def step(self) -> "Blizzard":
        destination = self.location.step(self.direction)
        new_location = self._opposite_side() if destination in WALLS else destination
        return Blizzard(location=new_location, direction=self.direction)

    def _opposite_side(self) -> Point2D:
        match self.direction:
            case "left":
                new_loc = Point2D(y=self.location.y, x=GRID_WIDTH - 1)
            case "right":
                new_loc = Point2D(y=self.location.y, x=1)
            case "up":
                new_loc = Point2D(x=self.location.x, y=GRID_HEIGHT - 1)
            case "down":
                new_loc = Point2D(x=self.location.x, y=1)
        return new_loc


class Blizzards:
    def __init__(self, initial_blizzards: List[Blizzard]) -> None:
        self._blizzards_store: Dict[int, list[Blizzard]] = {0: initial_blizzards}
        self._locations_store: Dict[int, set[Point2D]] = {
            0: {b.location for b in initial_blizzards}
        }

    def locations(self, elapsed_time: int) -> set[Point2D]:
        if elapsed_time not in self._locations_store:
            self._locations_store[elapsed_time] = {
                b.location for b in self.blizzards(elapsed_time=elapsed_time)
            }
        return self._locations_store[elapsed_time]

    def blizzards(self, elapsed_time: int) -> list[Blizzard]:
        if elapsed_time not in self._blizzards_store:
            self._blizzards_store[elapsed_time] = [
                b.step() for b in self.blizzards(elapsed_time=elapsed_time - 1)
            ]
        return self._blizzards_store[elapsed_time]


def parse_inputs(inputs: str) -> None:
    global WALLS
    global GRID_HEIGHT
    global GRID_WIDTH
    global DESTINATION
    blizzards = []
    for y, row in enumerate(inputs.splitlines()):
        for x, char in enumerate(row):
            match char:
                case "E":
                    continue
                case ".":
                    continue
                case "#":
                    WALLS.add(Point2D(x=x, y=y))
                case _:
                    blizzards.append(
                        Blizzard(location=Point2D(x=x, y=y), direction=DIRECTIONS[char])
                    )
    GRID_HEIGHT = max(w.y for w in WALLS)
    GRID_WIDTH = max(w.x for w in WALLS)
    DESTINATION = Point2D(x=GRID_WIDTH - 1, y=GRID_HEIGHT)
    return blizzards


@dataclass
class Config(State):
    location: Point2D
    blizzards: Blizzards
    elapsed_time: int = field(default=0)
    history: List[Point2D] = field(default_factory=list)

    def __lt__(self, other: "Config") -> bool:
        if self.elapsed_time == other.elapsed_time:
            return self._dist_to_dest() < other._dist_to_dest()
        return self.elapsed_time < other.elapsed_time

    def is_valid(self) -> bool:
        return True

    def _dist_to_dest(self) -> int:
        return abs(self.location - DESTINATION)

    def is_complete(self) -> bool:
        return self.location == DESTINATION

    def __str__(self):
        return f"{self.elapsed_time=}, {self.location=}"

    def all_possible_next_states(self) -> Iterable["Config"]:
        new_time = self.elapsed_time + 1
        new_history = self.history[:] + [self.location]

        kwargs = dict(
            elapsed_time=new_time, blizzards=self.blizzards, history=new_history
        )
        for dest in self.location.nb4():
            if dest in self.blizzards.locations(new_time) or dest in WALLS:
                continue
            if dest.y < 0:  # Exiting through the entrance
                continue
            yield Config(location=dest, **kwargs)

        if self.location not in self.blizzards.locations(new_time):
            yield Config(location=self.location, **kwargs)


def run(inputs: str) -> int:
    initial_blizzards = parse_inputs(inputs)
    blizzards = Blizzards(initial_blizzards=initial_blizzards)

    initial_state = Config(location=Point2D(x=1, y=0), blizzards=blizzards)

    best_route = a_star(initial_state=initial_state)
    return best_route.elapsed_time
