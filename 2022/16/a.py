import re
from typing import Dict, Optional, Set

import networkx as nx
from a_star import State, a_star

REG = re.compile(
    r"^Valve (\w+) has flow rate=(\d+); tunnel(?:s*) lead(?:s*) to valve(?:s*) (.+)$"
)

VALVES: Dict[str, int] = {}
DISTANCES: Dict[str, Dict[str, int]] = None
THRESHOLD: int = 0
TIME: int = 30


class Config(State):
    def __init__(
        self,
        location: str,
        elapsed_time: int = 0,
        released: int = 0,
        total_flow_rate: int = 0,
        open_valves: Optional[Set[str]] = None,
    ) -> None:
        self.location = location
        self.total_flow_rate = total_flow_rate
        self.open_valves = open_valves or set()
        self.elapsed_time = elapsed_time
        self.released = released

    def all_possible_next_states(self):
        for dest in VALVES:
            if dest in self.open_valves:
                continue
            move_and_open_time = DISTANCES[self.location][dest]
            yield Config(
                location=dest,
                elapsed_time=self.elapsed_time + move_and_open_time,
                released=self.released + self.total_flow_rate * move_and_open_time,
                total_flow_rate=self.total_flow_rate + VALVES[dest],
                open_valves=self.open_valves.union([dest]),
            )
        yield Config(
            location=self.location,
            elapsed_time=self.elapsed_time + 1,
            released=self.released + self.total_flow_rate,
            total_flow_rate=self.total_flow_rate,
            open_valves=self.open_valves,
        )

    def is_complete(self):
        return self.elapsed_time == TIME

    def is_valid(self):
        if self.elapsed_time > TIME:
            return False
        self.guaranteed()
        return self.potential() >= THRESHOLD

    def __lt__(self, other: "Config") -> bool:
        if self.elapsed_time == other.elapsed_time:
            return self.released > other.released
        return self.elapsed_time < other.elapsed_time

    def potential(self):
        # Other configs should only be one or two steps behind so consider what they can do in that time
        remaining_rates = max(v for k, v in VALVES.items() if k not in self.open_valves)
        best_potential = self.time_to_go * remaining_rates
        return self.released + self.total_flow_rate * self.time_to_go + best_potential

    @property
    def time_to_go(self):
        return max(TIME - self.elapsed_time, 0)

    def guaranteed(self):
        global THRESHOLD
        g = self.released + self.total_flow_rate * self.time_to_go
        THRESHOLD = max(THRESHOLD, g)

    def tag(self):
        return f"{self.location}, {sorted(self.open_valves)}, {self.elapsed_time}, {self.released}"

    def __str__(self):
        return f"{self.location}, {self.open_valves}, {self.released}, {self.elapsed_time}, {self.history}"


def run(inputs):

    global VALVES
    global DISTANCES

    graph = nx.Graph()

    for line in inputs.splitlines():
        name, rate, leads_to = REG.findall(line)[0]
        VALVES[name] = int(rate)
        [
            graph.add_edge(name, lt, weight=1)
            for lt in [l.strip() for l in leads_to.split(",")]
        ]

    DISTANCES = {
        origin: {
            dest: nx.shortest_path_length(graph, origin, dest, "weight") + 1
            for dest in VALVES
        }
        for origin in VALVES
    }

    inital_state = Config(location="AA")

    best_route = a_star(initial_state=inital_state, tag_func=lambda x: x.tag())

    return best_route.released
