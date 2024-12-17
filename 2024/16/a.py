from tools.a_star import State, a_star
from tools.inputs import parse_grid

GRID: dict[complex, str] = {}


class MapState(State):
    def __init__(self, position: complex, direction: complex, score: int = 0):
        self.position = position
        self.direction = direction
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

    def all_possible_next_states(self):
        yield MapState(self.position + self.direction, self.direction, self.score + 1)
        if self.direction.real:
            new_directions = [1j, -1j]
        else:
            new_directions = [1, -1]
        for new_direction in new_directions:
            yield MapState(self.position, new_direction, self.score + 1_000)

    def is_valid(self):
        return self.position in GRID and GRID[self.position] != "#"

    def is_complete(self):
        return GRID[self.position] == "E"

    def __hash__(self):
        return hash((self.position, self.direction))


def run(inputs: str) -> str:
    global GRID
    GRID = parse_grid(inputs)
    initial_state = MapState(next(k for k, v in GRID.items() if v == "S"), 1)
    best_route = a_star(initial_state=initial_state, tag_func=hash)
    return best_route.score
