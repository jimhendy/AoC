from collections import defaultdict, deque
from dataclasses import dataclass

from tools.point import Point2D

DESTINATION = Point2D(0, 0)
CONNECTIONS: dict[Point2D, dict[Point2D, int]] = {}


@dataclass(slots=True)
class State:
    position: Point2D
    history: set[Point2D]
    steps: int = 0

    def is_complete(self) -> bool:
        return self.position == DESTINATION

    def all_possible_next_states(self) -> list["State"]:
        history = self.history.union({self.position})
        for next_location, extra_steps in CONNECTIONS[self.position].items():
            if next_location not in history:
                yield State(next_location, history, self.steps + extra_steps)


def run(inputs: str) -> int:
    global DESTINATION
    start = None
    all_spaces = set()
    for y, line in enumerate(inputs.splitlines()):
        for x, char in enumerate(line):
            point = Point2D(x, y)
            if not y and start is None and char == ".":
                start = point
            if char == ".":
                DESTINATION = point
            if char != "#":
                all_spaces.add(point)

    # Using the above, construct a dict of point to a list of points that are connected to it
    for point in all_spaces:
        CONNECTIONS[point] = defaultdict(int)
        for next_point in point.nb4():
            if next_point in all_spaces:
                CONNECTIONS[point][next_point] = 1

    # Now, we can remove any points that have only two connections
    # Note, we must replace the connections to the point with the connections to the other two points
    for point in all_spaces:
        connected_points = CONNECTIONS[point]
        if len(connected_points) == 2:
            a, b = connected_points.keys()
            extra_steps = connected_points[a] + connected_points[b]
            del CONNECTIONS[a][point]
            del CONNECTIONS[b][point]
            CONNECTIONS[a][b] = extra_steps
            CONNECTIONS[b][a] = extra_steps
            del CONNECTIONS[point]

    initial_state = State(start, set())
    queue = deque([initial_state])
    complete = []

    while queue:
        state = queue.popleft()
        if state.is_complete():
            complete.append(state)
        else:
            for s in state.all_possible_next_states():
                queue.append(s)

    return max(c.steps for c in complete)
