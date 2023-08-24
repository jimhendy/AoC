import re
from dataclasses import dataclass
from typing import Dict, List, Optional

from a_star import State, a_star

REG = re.compile(
    r"^Valve (\w+) has flow rate=(\d+); tunnel(?:s*) lead(?:s*) to valve(?:s*) (.+)$"
)


@dataclass
class Valve:
    name: str
    rate: int
    leads_to: List[str]


VALVES: Dict[str, Valve] = {}
THRESHOLD: int = 0
TIME: int = 26


class Config(State):
    def __init__(
        self,
        location: str,
        el_location: str,
        elapsed_time: int = 0,
        released: int = 0,
        total_flow_rate: int = 0,
        open_valves: Optional[List[str]] = None,
        history: str = "",
    ) -> None:
        self.location = location
        self.el_location = el_location
        self.total_flow_rate = total_flow_rate
        self.open_valves = open_valves or set()
        self.elapsed_time = elapsed_time
        self.released = released
        self.history = history
        self.history += f"{self.location}/{self.el_location}({self.elapsed_time}) "

    def all_possible_next_states(self):

        new_time = self.elapsed_time + 1
        new_released = self.released + self.total_flow_rate

        for my_dest in VALVES[self.location].leads_to:
            for el_dest in VALVES[self.el_location].leads_to:
                # print("Both Move")
                yield Config(
                    location=my_dest,
                    el_location=el_dest,
                    elapsed_time=new_time,
                    released=new_released,
                    total_flow_rate=self.total_flow_rate,
                    open_valves=self.open_valves.copy(),
                    history=self.history,
                )

                # print("El moves, I stay and open")
                if self.location not in self.open_valves:
                    yield Config(
                        location=self.location,
                        el_location=el_dest,
                        elapsed_time=new_time,
                        released=new_released,
                        total_flow_rate=self.total_flow_rate
                        + VALVES[self.location].rate,
                        open_valves=self.open_valves.union([self.location]),
                        history=self.history + "[i]",
                    )

            # print("I move, El stays and opens")
            if self.el_location not in self.open_valves:
                yield Config(
                    location=my_dest,
                    el_location=self.el_location,
                    elapsed_time=new_time,
                    released=new_released,
                    total_flow_rate=self.total_flow_rate
                    + VALVES[self.el_location].rate,
                    open_valves=self.open_valves.union([self.el_location]),
                    history=self.history + "[e]",
                )

        # print("Both stay and open")
        if (
            self.el_location not in self.open_valves
            and self.location not in self.open_valves
            and self.el_location != self.location
        ):
            yield Config(
                location=self.location,
                el_location=self.el_location,
                elapsed_time=new_time,
                released=new_released,
                total_flow_rate=self.total_flow_rate
                + VALVES[self.el_location].rate
                + VALVES[self.location].rate,
                open_valves=self.open_valves.union([self.el_location, self.location]),
                history=self.history + "[ie]",
            )

    def is_complete(self):
        return self.elapsed_time == TIME

    def is_valid(self):
        if self.elapsed_time > TIME:
            return False
        self.guaranteed()
        return self.potential() >= (THRESHOLD / 1)

    def __lt__(self, other: "Config") -> bool:
        if self.elapsed_time == other.elapsed_time:
            return self.released > other.released
        return self.elapsed_time < other.elapsed_time

    def potential(self):
        # Other configs should only be one or two steps behind so consider what they can do in that time
        remaining_rates = sorted(
            [v.rate for k, v in VALVES.items() if k not in self.open_valves],
            reverse=True,
        )
        best_potential = self.time_to_go * sum(remaining_rates[:2])
        return (
            self.released
            + self.total_flow_rate * self.time_to_go
            + best_potential / 1.01
        )

    @property
    def time_to_go(self):
        return max(TIME - self.elapsed_time, 0)

    def guaranteed(self):
        global THRESHOLD
        g = self.released + self.total_flow_rate * self.time_to_go
        THRESHOLD = max(THRESHOLD, g)

    def tag(self):
        return f"{self.location}, {self.el_location}, {self.total_flow_rate}, {self.released}"

    def __str__(self):
        return f"{self.location}/{self.el_location}, {self.open_valves}, {self.released}, {self.elapsed_time}, {self.history}"


def run(inputs):

    global VALVES

    for line in inputs.splitlines():
        name, rate, leads_to = REG.findall(line)[0]
        VALVES[name] = Valve(
            name=name, rate=int(rate), leads_to=[l.strip() for l in leads_to.split(",")]
        )

    inital_state = Config(location="AA", el_location="AA")

    best_route = a_star(initial_state=inital_state, tag_func=lambda x: x.tag())

    return best_route.released
