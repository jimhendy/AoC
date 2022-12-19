from functools import lru_cache
from typing import List, Optional

from a_star import AStarException, State, a_star

# ToDo: Add caching (fastest route from any position)
# Numba
# Remove classes / add slots
# Better algo working backwards

STEPS = [+1, -1, +1j, -1j]


class GridLocation(State):

    grid: List[List[int]]
    dest: complex

    def __init__(self, loc: complex, prev_locs: Optional[List[complex]] = None):
        self.loc = loc
        self.prev_locs = prev_locs or []

    def is_complete(self) -> bool:
        return self.loc == self.dest

    def is_valid(self):
        return True

    def __lt__(self, other: "GridLocation") -> bool:
        return len(self.prev_locs) < len(other.prev_locs)

    def all_possible_next_states(self):
        for step in STEPS:
            new_loc = self.loc + step
            if not 0 <= new_loc.real < self.grid_size().real:
                continue
            if not 0 <= new_loc.imag < self.grid_size().imag:
                continue
            dest_value = GridLocation.value_at_loc(new_loc)
            if dest_value - GridLocation.value_at_loc(self.loc) > 1:
                continue
            prev_loc = self.prev_locs[:]
            prev_loc.append(self.loc)
            yield GridLocation(loc=new_loc, prev_locs=prev_loc)

    @staticmethod
    def value_at_loc(loc: complex) -> int:
        return GridLocation.grid[int(loc.imag)][int(loc.real)]

    @staticmethod
    def set_value_at_loc(loc: complex, value) -> None:
        GridLocation.grid[int(loc.imag)][int(loc.real)] = value

    @staticmethod
    @lru_cache(maxsize=1)
    def grid_size() -> complex:
        return len(GridLocation.grid) * 1j + len(GridLocation.grid[0])

    @staticmethod
    def loc_of_value(value: int) -> complex:
        for y in range(int(GridLocation.grid_size().imag)):
            for x in range(int(GridLocation.grid_size().real)):
                c = x + 1j * y
                if GridLocation.value_at_loc(c) == value:
                    yield c


def run(inputs: str):
    GridLocation.grid = [list(map(ord, line)) for line in inputs.splitlines()]

    starting_loc = next(GridLocation.loc_of_value(ord("S")))
    desintation_loc = next(GridLocation.loc_of_value(ord("E")))

    GridLocation.set_value_at_loc(starting_loc, ord("a"))
    GridLocation.set_value_at_loc(desintation_loc, ord("z"))

    GridLocation.dest = desintation_loc

    possible_starting_points = list(GridLocation.loc_of_value(ord("a")))
    steps = []
    for starting_point in possible_starting_points:
        try:
            initial_state = GridLocation(loc=starting_point)
            optimal_route = a_star(
                initial_state=initial_state, tag_func=lambda gl: gl.loc
            )
            steps.append(len(optimal_route.prev_locs))
        except AStarException:
            pass

    return min(steps)
