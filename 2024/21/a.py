from collections import Counter, defaultdict
from collections.abc import Generator
from dataclasses import dataclass, field
from itertools import pairwise, permutations
from typing import ClassVar

from tools.a_star import State as AStarState
from tools.a_star import a_star
from tools.inputs import parse_list_of_lists

NUMPAD = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"],
]

DIR_PAD = [
    [None, "^", "A"],
    ["<", "v", ">"],
]


DIRECTIONS = {
    "v": 1j,
    "^": -1j,
    "<": -1,
    ">": 1,
}


@dataclass
class State(AStarState):
    loc: complex
    end: complex
    history: list[complex] = field(default_factory=list)

    grid: ClassVar[dict[complex, str | None]]

    def all_possible_next_states(self) -> Generator["State", None, None]:
        for dir_char, direction in DIRECTIONS.items():
            new_loc = self.loc + direction
            if new_loc not in self.grid:
                continue

            if self.grid[new_loc] is None:
                continue

            yield State(loc=new_loc, end=self.end, history=self.history + [dir_char])

    def is_complete(self) -> bool:
        return self.loc == self.end

    def __lt__(self, other: "State") -> bool:
        return len(self.history) < len(other.history)

    def is_valid(self) -> bool:
        return True


def _all_shortest_paths(
    grid: dict[complex, str | None],
) -> dict[complex, dict[complex, list[str]]]:
    State.grid = grid

    results = defaultdict(dict)

    for start, start_char in grid.items():
        if start_char is None:
            continue

        for dest, dest_char in grid.items():
            if dest_char is None:
                continue

            initial_state = State(
                loc=start,
                end=dest,
            )

            optimal_route = a_star(initial_state).history
            paths = {f"{''.join(perm)}A" for perm in permutations(optimal_route)}
            # Remove any paths with non-consecutive same directions
            # E.g. >>v NOT >v>
            non_consecutive_paths = []
            for p in paths:
                counts = Counter(p)
                if all(direction * counts[direction] in p for direction in DIRECTIONS):
                    non_consecutive_paths.append(p)

            # Ensure none of the paths ever set foot on a None
            non_none_paths = []
            for p in non_consecutive_paths:
                locations = [
                    start + sum(DIRECTIONS[direction] for direction in p[:i])
                    for i in range(1, len(p))
                ]
                if all(grid[loc] is not None for loc in locations):
                    non_none_paths.append(p)

            results[start][dest] = non_none_paths

    return results


def loc_in_grid(grid: dict[complex, str], character: str) -> complex:
    return next(loc for loc, char in grid.items() if char == character)


def encode(
    code: str,
    grid: dict[complex:str],
    paths: dict[complex, dict[complex, list[str]]],
) -> set[str]:
    results = {
        "",
    }
    for start_char, end_char in pairwise(code):
        start = loc_in_grid(grid, start_char)
        end = loc_in_grid(grid, end_char)
        results = {res + path for res in results for path in paths[start][end]}

        shortest_result = min(results, key=len)
        results = {r for r in results if len(r) == len(shortest_result)}

    return results


def extract_numeric(code: str) -> int:
    return int("".join(char for char in code if char.isdigit()))


def run(inputs: str) -> int:
    num_grid = parse_list_of_lists(NUMPAD)
    num_paths = _all_shortest_paths(num_grid)

    dir_grid = parse_list_of_lists(DIR_PAD)
    dir_paths = _all_shortest_paths(dir_grid)

    total = 0

    for code in inputs.splitlines():
        numeric = extract_numeric(code)

        codes = encode(f"A{code}", num_grid, num_paths)
        breakpoint()
        for _ in range(2):
            codes = [
                c for code in codes for c in encode(f"A{code}", dir_grid, dir_paths)
            ]
            min_len = min(len(c) for c in codes)
            codes = [c for c in codes if len(c) == min_len]

        total += numeric * len(codes[0])

    return total
