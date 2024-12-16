from tools.a_star import State
from tools.inputs import parse_grid
import heapq

GRID: dict[complex, str] = {}


class MapState(State):
    def __init__(
        self,
        position: complex,
        direction: complex,
        score: int = 0,
        history: list[complex] | None = None,
    ):
        self.position = position
        self.direction = direction
        self.score = score
        self.history = history or []

    def __lt__(self, other):
        return self.score < other.score

    def all_possible_next_states(self):
        yield MapState(
            self.position + self.direction,
            self.direction,
            self.score + 1,
            self.history + [self.position],
        )
        if self.direction.real:
            new_directions = [1j, -1j]
        else:
            new_directions = [1, -1]
        for new_direction in new_directions:
            yield MapState(
                self.position,
                new_direction,
                self.score + 1_000,
                self.history + [self.position],
            )

    def is_valid(self):
        return self.position in GRID and GRID[self.position] != "#"

    def is_complete(self):
        return GRID[self.position] == "E"

    def __hash__(self):
        return hash((self.position, self.direction))


def all_possible_routes(initial_state: MapState):
    possible_states = [initial_state]
    seen = set()
    complete = []

    while possible_states:
        best_option = heapq.heappop(possible_states)
        if best_option.is_complete():
            complete.append(best_option)
            continue

        for s in best_option.all_possible_next_states():
            if not s.is_valid():
                continue
            tag = hash(s)
            if tag in seen:
                continue
            seen.add(tag)
            heapq.heappush(possible_states, s)

    return complete


def run(inputs: str) -> int:
    global GRID
    GRID = parse_grid(inputs)
    initial_state = MapState(next(k for k, v in GRID.items() if v == "S"), 1)
    # Find ALL possible routes, no need to stop at the first one
    all_routes = all_possible_routes(initial_state)
    all_route_tiles = set(tile for route in all_routes for tile in route.history)
    return len(all_route_tiles)
