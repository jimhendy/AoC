import os
from collections import defaultdict, deque


class Route:
    def __init__(self, current_loc, connections, visits=None):
        self.current_loc = current_loc
        self.visits = visits or defaultdict(int)
        self.visits[self.current_loc] += 1
        self.connections = connections

    def all_possible_next_states(self):
        for next_loc in self.connections[self.current_loc]:

            if self.visits[next_loc] and next_loc.islower():
                continue

            yield Route(
                next_loc,
                self.connections,
                visits=self.visits.copy(),
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
