from tools.a_star import State, a_star

GRID_SIZE = 70
N_BYTES = 1024
BYTES: set[complex] = set()


class MapState(State):
    def __init__(
        self,
        loc: complex,
        steps: int = 0,
        history: set[complex] | None = None,
    ):
        self.loc = loc
        self.steps = steps
        self.history = history or set()
        self.history.add(loc)

    def all_possible_next_states(self):
        for direction in [1j, -1j, 1, -1]:
            new_loc = self.loc + direction
            if (
                0 <= new_loc.real <= GRID_SIZE
                and 0 <= new_loc.imag <= GRID_SIZE
                and new_loc not in BYTES
            ):
                yield MapState(
                    loc=new_loc,
                    steps=self.steps + 1,
                    history=self.history.copy(),
                )

    def is_complete(self):
        return self.loc == complex(GRID_SIZE, GRID_SIZE)

    def is_valid(self):
        return True

    def __str__(self):
        return f"{self.loc}"

    def __lt__(self, other):
        return self.steps < other.steps


def run(inputs: str) -> int:
    global BYTES
    upcoming_bytes = set()
    for line_num, line in enumerate(inputs.splitlines()):
        byte = complex(*map(int, line.split(",")))
        if line_num >= N_BYTES:
            upcoming_bytes.add(byte)
        else:
            BYTES.add(byte)

    last_added_byte = None
    while True:
        try:
            route = a_star(
                initial_state=MapState(loc=0),
            )
        except Exception:
            return f"{last_added_byte.real:.0f},{last_added_byte.imag:.0f}"

        added_bytes = []
        for new_byte in upcoming_bytes:
            if new_byte not in route.history:
                added_bytes.append(new_byte)
            else:
                break

        if not added_bytes:
            next_byte = next(iter(upcoming_bytes))
            added_bytes.append(next_byte)

        # Remove added bytes from upcoming_bytes
        for added_byte in added_bytes:
            upcoming_bytes.remove(added_byte)
            last_added_byte = added_byte
            BYTES.add(added_byte)
