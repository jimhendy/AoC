from collections import deque
from dataclasses import dataclass, field

from tools.a_star import State, a_star
from tools.inputs import parse_grid

GRID: dict[complex, str] = {}


@dataclass(slots=True)
class MapState(State):
    position: complex
    direction: complex
    score: int = 0
    history: list[tuple[complex, complex]] = field(default_factory=list)

    def __lt__(self, other):
        return self.score < other.score

    def all_possible_next_states(self):
        if (
            GRID.get(self.position + self.direction) != "#"
            and (self.position + self.direction, self.direction) not in self.history
        ):
            yield MapState(
                self.position + self.direction,
                self.direction,
                self.score + 1,
                self.history + [self.tag()],
            )
        if self.direction.real:
            new_directions = [1j, -1j]
        else:
            new_directions = [1, -1]
        for new_direction in new_directions:
            if (
                GRID.get(self.position + new_direction) != "#"
                and (self.position, new_direction) not in self.history
            ):
                yield MapState(
                    self.position,
                    new_direction,
                    self.score + 1_000,
                    self.history + [self.tag()],
                )

    def tag(self):
        return (self.position, self.direction)

    def is_valid(self):
        return (
            self.position in GRID
            and GRID[self.position] != "#"
            and self.tag() not in self.history
        )

    def is_complete(self):
        return GRID[self.position] == "E"

    def __hash__(self):
        return hash(self.tag())


def all_routes_below_score(initial_state: MapState, max_score: int) -> list[MapState]:
    possible_states = deque([initial_state])
    complete = []
    lowest_score_to_get_here = {}

    while possible_states:
        best_option = possible_states.popleft()

        if best_option.tag() in lowest_score_to_get_here:
            if best_option.score > lowest_score_to_get_here[best_option.tag()]:
                continue
            lowest_score_to_get_here[best_option.tag()] = best_option.score
        else:
            lowest_score_to_get_here[best_option.tag()] = best_option.score

        if best_option.is_complete():
            if best_option.score == max_score:
                complete.append(best_option)
            else:
                assert best_option.score > max_score
                break

        for s in best_option.all_possible_next_states():
            if s.score <= max_score:  # and s.is_valid():
                possible_states.append(s)

    return complete


def run(inputs: str) -> int:
    global GRID
    GRID = parse_grid(inputs)
    initial_state = MapState(next(k for k, v in GRID.items() if v == "S"), 1)

    # FInd the best route
    best_routes = [a_star(initial_state, tag_func=hash)]
    best_score = best_routes[-1].score
    print(f"Initial best route found with score {best_score}")

    all_routes = all_routes_below_score(initial_state, best_score)

    all_route_tiles = set(tile for route in all_routes for tile, *_ in route.history)

    return len(all_route_tiles) + 1
