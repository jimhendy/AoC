from tools.a_star import a_star, State

GRID_SIZE = 70
N_BYTES = 1024
BYTES: set[complex] = set()


class MapState(State):
    def __init__(self, loc: complex, steps: int = 0):
        self.loc = loc
        self.steps = steps

    def all_possible_next_states(self):
        for direction in [1j, -1j, 1, -1]:
            new_loc = self.loc + direction
            if (
                0 <= new_loc.real <= GRID_SIZE
                and 0 <= new_loc.imag <= GRID_SIZE
                and new_loc not in BYTES
            ):
                yield MapState(loc=new_loc, steps=self.steps + 1)

    def is_complete(self):
        return self.loc == complex(GRID_SIZE, GRID_SIZE)

    def is_valid(self):
        return True

    def __str__(self):
        return f"{self.loc}"

    def __lt__(self, other):
        return self.steps < other.steps


def print_map(loc: complex):
    for y in range(GRID_SIZE + 1):
        for x in range(GRID_SIZE + 1):
            if x == loc.real and y == loc.imag:
                print("X", end="")
            elif complex(x, y) in BYTES:
                print("#", end="")
            else:
                print(".", end="")
        print()


def run(inputs: str) -> int:
    global BYTES
    for line_num, line in enumerate(inputs.splitlines()):
        if line_num >= N_BYTES:
            break
        BYTES.add(complex(*map(int, line.split(","))))

    return a_star(
        initial_state=MapState(loc=0),
    ).steps
