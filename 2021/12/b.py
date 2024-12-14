import os
from collections import defaultdict, deque

LOWER_CASE = set()


class Route:
    def __init__(
        self,
        current_loc,
        connections,
        visits=None,
        has_double_lower_visit=False,
    ) -> None:
        self.current_loc = current_loc
        self.visits = visits or defaultdict(int)
        self.visits[self.current_loc] += 1
        self.connections = connections
        self.has_double_lower_visit = has_double_lower_visit
        if not self.has_double_lower_visit:
            for k, v in self.visits.items():
                if v == 2 and k in LOWER_CASE:
                    self.has_double_lower_visit = True
                    break

    def all_possible_next_states(self):
        for next_loc in self.connections[self.current_loc]:
            prev_visits = self.visits[next_loc]
            if prev_visits and next_loc in LOWER_CASE:
                if prev_visits == 2 or (prev_visits and self.has_double_lower_visit):
                    continue

            yield Route(
                next_loc,
                self.connections,
                visits=self.visits.copy(),
                has_double_lower_visit=self.has_double_lower_visit,
            )

    def is_complete(self):
        return self.current_loc == "end"


def extract_connections(inputs):
    connections = defaultdict(list)
    for line in inputs.split(os.linesep):
        a, b = line.split("-")
        if b != "start" and a != "end":
            connections[a].append(b)
        if a != "start" and b != "end":
            connections[b].append(a)
    return connections


def run(inputs):
    connections = extract_connections(inputs)
    [LOWER_CASE.add(k) for k in connections if k.islower()]
    queue = deque([Route("start", connections)])
    n_routes = 0

    while queue:
        considered_route = queue.pop()
        if considered_route.is_complete():
            n_routes += 1
            continue
        for next_route in considered_route.all_possible_next_states():
            queue.append(next_route)

    return n_routes
