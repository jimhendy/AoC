from functools import lru_cache

from a_star import State, a_star

STEPS = [+1, -1, +1j, -1j]


class GridLocation(State):
    grid: list[list[int]]
    dest: complex

    def __init__(self, loc: complex, prev_locs: list[complex] | None = None) -> None:
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
                    return c
        return None


def run(inputs: str):
    GridLocation.grid = [list(map(ord, line)) for line in inputs.splitlines()]

    starting_loc = GridLocation.loc_of_value(ord("S"))
    desintation_loc = GridLocation.loc_of_value(ord("E"))

    GridLocation.set_value_at_loc(starting_loc, ord("a"))
    GridLocation.set_value_at_loc(desintation_loc, ord("z"))

    GridLocation.dest = desintation_loc

    initial_state = GridLocation(loc=starting_loc)

    optimal_route = a_star(initial_state=initial_state, tag_func=lambda gl: gl.loc)

    return len(optimal_route.prev_locs)
