import re
from dataclasses import dataclass, field
from functools import cached_property
from typing import ClassVar

from a_star import State, a_star

REG = re.compile(
    r"^Valve (\w+) has flow rate=(\d+); tunnel(?:s*) lead(?:s*) to valve(?:s*) (.+)$",
)


@dataclass(slots=True, frozen=True)
class Valve:
    name: str
    rate: int
    leads_to: dict[str, int]  # Desination, Duration


@dataclass(slots=True, frozen=True)
class Actor:
    location: str
    time_to_action: int


VALVES: dict[str, Valve] = {}
TIME: int = 26


@dataclass(slots=True, frozen=True)
class Config(State):
    person: Actor
    elephant: Actor

    elapsed_time: int = 0
    released: int = 0
    total_flow_rate: int = 0

    open_valves: set[str] = field(default_factory=set)

    _threshold: ClassVar[int] = 0

    def all_possible_next_states(self):
        new_time = self.elapsed_time + 1
        new_released = self.released + self.total_flow_rate

        for my_dest in VALVES[self.location].leads_to:
            for el_dest in VALVES[self.el_location].leads_to:
                yield Config(
                    location=my_dest,
                    el_location=el_dest,
                    elapsed_time=new_time,
                    released=new_released,
                    total_flow_rate=self.total_flow_rate,
                    open_valves=self.open_valves.copy(),
                    history=self.history,
                )

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
        return self.potential >= Config._threshold

    def __lt__(self, other: "Config") -> bool:
        return self.elapsed_time < other.elapsed_time

    @cached_property
    def potential(self):
        # Other configs should only be one or two steps behind so consider what they
        # can do in that time
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

    @cached_property
    def time_to_go(self):
        return max(TIME - self.elapsed_time, 0)

    def guaranteed(self):
        guaranteed = self.released + self.total_flow_rate * self.time_to_go
        Config._threshold = max(Config._threshold, guaranteed)

    @cached
    def tag(self):
        return (
            f"{self.location}, {self.el_location}, "
            f"{self.total_flow_rate}, {self.released}"
        )

    def __str__(self) -> str:
        return (
            f"{self.location}/{self.el_location}, {self.open_valves}, "
            f"{self.released}, {self.elapsed_time}, {self.history}"
        )


def run(inputs):
    for line in inputs.splitlines():
        name, rate, leads_to = REG.findall(line)[0]
        rate = int(rate)
        VALVES[name] = Valve(
            name=name,
            rate=rate,
            leads_to=[l.strip() for l in leads_to.split(",")],
        )

    inital_state = Config(location="AA", el_location="AA")

    best_route = a_star(initial_state=inital_state, tag_func=lambda x: x.tag())

    return best_route.released
