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


def distance(a: complex, b: complex) -> int:
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def print_grid(
    grid: set[complex], start: complex, end: complex, highlight: set[complex] = set()
):
    width = max(int(loc.real) for loc in grid) + 2
    height = max(int(loc.imag) for loc in grid) + 2
    for y in range(height):
        for x in range(width):
            loc = complex(x, y)
            if loc == start:
                print("S", end="")
            elif loc == end:
                print("E", end="")
            elif loc in highlight:
                print("H", end="")
            elif loc in grid:
                print(".", end="")
            else:
                print("#", end="")
        print()


def time_saved_by_cheating(history: dict[complex, int], loc: complex) -> list[int]:
    start = history[loc]
    return [
        history[end] - distance(end, loc) - start
        for end in PATHS
        if distance(end, loc) <= 20
    ]


def run(inputs: str) -> int:
    global PATHS, END
    PATHS = parse_grid(inputs, blacklist="#")

    start = loc_in_grid(inputs, "S")
    END = loc_in_grid(inputs, "E")

    nominal_route = a_star(MapState(loc=start))

    hist_dict = {loc: i for i, loc in enumerate(nominal_route.history)}
    import tqdm

    times = [time_saved_by_cheating(hist_dict, loc) for loc in tqdm.tqdm(hist_dict)]
    return sum(time >= 100 for time in chain(*times))
