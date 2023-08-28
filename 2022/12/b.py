from functools import lru_cache

from a_star import State, a_star

STEPS = [+1, -1, +1j, -1j]
ord_S = ord("S")
ord_E = ord("E")
ord_a = ord("a")
ord_z = ord("z")


class Grid:
    def __init__(self, inputs: str) -> None:
        self._values = [list(map(ord, line)) for line in inputs.splitlines()]

    @lru_cache(maxsize=2056)
    def __getitem__(self, loc: complex) -> int:
        return self._values[int(loc.imag)][int(loc.real)]

    def __setitem__(self, loc: complex, value: int) -> None:
        self._values[int(loc.imag)][int(loc.real)] = value

    def locate(self, *args) -> dict[int, complex]:
        flat_values = [char for row in self._values for char in row]
        return {
            a: complex(*(divmod(flat_values.index(a), len(self._values[0]))[::-1]))
            for a in args
        }


class GridLocation(State):
    grid: Grid
    grid_width: int
    grid_height: int

    def __init__(self, loc: complex, n_steps: int = 0) -> None:
        self.loc = loc
        self.n_steps = n_steps
        self._loc_value = self.grid[self.loc]

    def is_complete(self) -> bool:
        return self._loc_value == ord_a

    def is_valid(self):
        return True

    def __lt__(self, other: "GridLocation") -> bool:
        return self.n_steps < other.n_steps

    def all_possible_next_states(self):
        for step in STEPS:
            new_loc = self.loc + step
            if not (0 <= new_loc.real < self.grid_width):
                continue
            if not (0 <= new_loc.imag < self.grid_height):
                continue
            dest_value = self.grid[new_loc]
            if dest_value - self._loc_value < -1:
                continue
            yield GridLocation(loc=new_loc, n_steps=self.n_steps + 1)


def run(inputs: str):
    grid = Grid(inputs)

    locs = grid.locate(ord_S, ord_E)

    grid[locs[ord_S]] = ord_a
    grid[locs[ord_E]] = ord_z

    GridLocation.grid = grid
    GridLocation.grid_width = len(grid._values[0])
    GridLocation.grid_height = len(grid._values)
    initial_state = GridLocation(loc=locs[ord_E])

    optimal_route = a_star(initial_state=initial_state, tag_func=lambda gl: gl.loc)

    return optimal_route.n_steps
