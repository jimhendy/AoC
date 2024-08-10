from dataclasses import dataclass
from queue import SimpleQueue

from tools.point import Point2D

SLOPES = {
    "^": Point2D(0, -1),
    "v": Point2D(0, 1),
    ">": Point2D(1, 0),
    "<": Point2D(-1, 0),
}
WALL = "#"
DESTINATION = Point2D(0, 0)
MAP: dict[Point2D, str] = {}


@dataclass(slots=True)
class State:
    position: Point2D
    history: set[Point2D]

    def _would_be_valid(self, position: Point2D) -> bool:
        if position not in MAP:
            return False
        if MAP[position] == WALL:
            return False
        if position in self.history:
            return False
        return True

    def is_complete(self) -> bool:
        return self.position == DESTINATION

    def all_possible_next_states(self) -> list["State"]:
        current_location_value = MAP[self.position]
        history = self.history.union({self.position})
        if current_location_value in SLOPES:
            next_location = self.position + SLOPES[current_location_value]
            if self._would_be_valid(next_location):
                yield State(next_location, history)
        else:
            for next_location in self.position.nb4():
                if self._would_be_valid(next_location):
                    yield State(next_location, history)


def run(inputs: str) -> int:
    global DESTINATION
    start = None
    for y, line in enumerate(inputs.splitlines()):
        for x, char in enumerate(line):
            point = Point2D(x, y)
            if not y and start is None and char == ".":
                start = point
            if char == ".":
                DESTINATION = point
            MAP[point] = char
    initial_state = State(start, set())

    states = SimpleQueue()
    states.put(initial_state)
    complete = []
    while not states.empty():
        best_option = states.get()
        if best_option.is_complete():
            complete.append(best_option)
        else:
            for s in best_option.all_possible_next_states():
                states.put(s)

    return max(len(c.history) for c in complete)
