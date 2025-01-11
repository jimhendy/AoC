from tools.inputs import parse_grid, loc_in_grid
from tools.a_star import State, a_star
from dataclasses import dataclass, field
import heapq
from collections import defaultdict, Counter
from itertools import chain

PATHS: set[complex] = set()
END: complex = complex(0, 0)


@dataclass
class MapState(State):
    loc: complex
    steps: int = 0
    history: list[complex] = field(default_factory=list)

    def __post_init__(self):
        self.history.append(self.loc)

    def all_possible_next_states(self):
        for direction in [1j, -1j, 1, -1]:
            new_loc = self.loc + direction
            if new_loc in PATHS:
                yield MapState(
                    loc=new_loc, steps=self.steps + 1, history=self.history.copy()
                )

    def is_complete(self):
        return self.loc == END

    def is_valid(self):
        return True

    def __str__(self):
        return f"{self.loc}"

    def __lt__(self, other):
        return self.steps < other.steps


def time_saved_by_cheating(history: dict[complex, int], loc: complex) -> list[int]:
    times = []
    start = history[loc]
    for direction in [1j, -1j, 1, -1]:
        new_loc = loc + direction * 2
        if new_loc in history:
            end = history[new_loc] - 2
            if end > start:
                times.append(end - start)
    return times


def run(inputs: str) -> int:
    global PATHS, END
    PATHS = parse_grid(inputs, blacklist="#")

    start = loc_in_grid(inputs, "S")
    END = loc_in_grid(inputs, "E")

    nominal_route = a_star(MapState(loc=start))

    hist_dict = {loc: i for i, loc in enumerate(nominal_route.history)}

    times = [time_saved_by_cheating(hist_dict, loc) for loc in hist_dict]

    return sum(time >= 100 for time in chain(*times))
