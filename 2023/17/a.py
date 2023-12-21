from collections.abc import Iterable
from functools import cache
from typing import Self
from uuid import uuid4

from tools.a_star import State, a_star


class Point2D(complex):
    @property
    def x(self) -> int:
        return int(self.real)

    @property
    def y(self) -> int:
        return int(self.imag)

    def __add__(self, other: Self) -> Self:
        return Point2D(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other: Self) -> Self:
        return Point2D(self.real - other.real, self.imag - other.imag)


class Crucible(State):
    max_x: int = 0
    max_y: int = 0
    grid: list[list[int]] = []

    def __init__(
        self,
        position: Point2D,
        history: list[Point2D] | None = None,
        previous_heat_loss: int = 0,
    ):
        self.position = position
        self.history = history or []
        self.previous_heat_loss = previous_heat_loss
        self.direction = None if not self.history else self.position - self.history[-1]

    @cache
    def _num_forward_steps(self):
        total = 0
        for to_, from_ in zip(self.history[::-1], self.history[:-1][::-1]):
            if (to_ - from_) == self.direction:
                total += 1
            else:
                break
        return total

    @cache
    def _can_go_forwards(self):
        return self._num_forward_steps() < 2

    @cache
    def heat_loss(self) -> int:
        return self.previous_heat_loss + self.grid[self.position.y][self.position.x]

    def __lt__(self, other: Self) -> bool:
        return self.heat_loss() < other.heat_loss()

    @staticmethod
    def _valid_location(location: Point2D) -> bool:
        return (0 <= location.x <= Crucible.max_x) and (
            0 <= location.y <= Crucible.max_y
        )

    def is_valid(self) -> bool:
        return self._valid_location(self.position)

    def is_complete(self) -> bool:
        return self.position == Point2D(self.max_x, self.max_y)

    @cache
    def _allowed_directions(self) -> list[Point2D] | str:
        if not self.direction:
            return uuid4()
        if self.direction.x and self.direction.y:
            raise ValueError("Invalid direction: " + str(self.direction))
        horizontal = bool(self.direction.x)
        directions = []
        if horizontal:
            if self._valid_location(self.position + Point2D(0, -1)):
                directions.append(Point2D(0, -1))
            if self._valid_location(self.position + Point2D(0, 1)):
                directions.append(Point2D(0, 1))
        else:
            if self._valid_location(self.position + Point2D(-1, 0)):
                directions.append(Point2D(-1, 0))
            if self._valid_location(self.position + Point2D(1, 0)):
                directions.append(Point2D(1, 0))
        if self._can_go_forwards():
            new_location = self.position + self.direction
            if self._valid_location(new_location):
                directions.append(self.direction)
        return directions

    def next_state(self, direction: Point2D) -> Self | None:
        return Crucible(
            position=self.position + direction,
            history=self.history + [self.position],
            previous_heat_loss=self.heat_loss(),
        )

    def all_possible_next_states(self) -> Iterable[State]:
        if len(self.history):
            for direction in self._allowed_directions():
                yield self.next_state(direction)
        else:
            # Initial state
            for dx in [-1, 1]:
                state = Crucible(
                    position=self.position + Point2D(dx, 0),
                    history=[self.position],
                )
                if state.is_valid():
                    yield state
            for dy in [-1, 1]:
                state = Crucible(
                    position=self.position + Point2D(0, dy),
                    history=[self.position],
                )
                if state.is_valid():
                    yield state

    def __str__(self):
        include_data = [
            self.position,
            self._allowed_directions(),
            self._num_forward_steps(),
        ]
        output = f"{self.__class__.__name__}(" + ",".join(map(str, include_data)) + ")"
        return output

    def draw_route(self):
        symbols = {}
        for j, i in zip(self.history, self.history[1:] + [self.position]):
            direction = i - j
            symbol = {
                1: ">",
                -1: "<",
                Point2D(0, 1): "v",
                Point2D(0, -1): "^",
            }[direction]
            symbols[i] = symbol
        for y in range(self.max_y + 1):
            line = ""
            for x in range(self.max_x + 1):
                line += symbols.get(Point2D(x, y), str(self.grid[y][x]))
            print(line)


def run(inputs: str) -> int:
    Crucible.grid = list(list(map(int, line)) for line in inputs.splitlines())
    Crucible.max_x = len(Crucible.grid[0]) - 1
    Crucible.max_y = len(Crucible.grid) - 1

    initial_state = Crucible(position=Point2D(0, 0))

    route = a_star(initial_state)

    return route.heat_loss()
