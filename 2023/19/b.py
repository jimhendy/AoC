import operator
from dataclasses import dataclass

import networkx as nx

POSSIBLE_VALUES = 4_000
A_INDEX = 0
ACCEPTED_DESTINATIONS = set()


@dataclass(slots=True)
class Range:
    min: int = 1
    max: int = POSSIBLE_VALUES

    def set_min(self, min_: int) -> None:
        self.min = max(self.min, min_)
        if self.min > self.max:
            raise ValueError(f"{self.min=} > {self.max=}")

    def set_max(self, max_: int) -> None:
        self.max = min(self.max, max_)
        if self.max < self.min:
            raise ValueError(f"{self.max=} < {self.min=}")

    def num_values(self) -> int:
        if self.min >= self.max:
            return 0
        return self.max - self.min + 1


@dataclass(frozen=True, slots=True)
class Rule:
    destination: str
    attrtibute: str | None = None
    comparison: operator.attrgetter | None = None
    value: int | None = None

    @staticmethod
    def _destination(destination: str) -> str:
        global A_INDEX
        global ACCEPTED_DESTINATIONS

        destination = destination.strip()

        if destination == "A":
            destination += f"_{A_INDEX}"
            A_INDEX += 1
            ACCEPTED_DESTINATIONS.add(destination)

        return destination

    @classmethod
    def from_str(cls, line: str) -> "Rule":
        global A_INDEX
        global ACCEPTED_DESTINATIONS
        if ":" not in line:
            return cls(destination=cls._destination(line))
        condition, destination = line.split(":")

        destination = cls._destination(destination)

        comparison = {
            ">": operator.gt,
            "<": operator.lt,
        }[condition[1]]

        return cls(
            destination=destination.strip(),
            attrtibute=condition[0],
            comparison=comparison,
            value=int(condition[2:]),
        )


@dataclass(frozen=True, slots=True)
class Workflow:
    name: str
    rules: list[Rule]

    @classmethod
    def from_line(cls, line: str) -> "Workflow":
        name, rules = line.split("{")
        rules = rules[:-1].split(",")
        rules = [Rule.from_str(rule) for rule in rules]
        return cls(
            name=name,
            rules=rules,
        )


def run(inputs: str) -> int:
    workflows: dict[str, Workflow] = {}
    graph = nx.DiGraph(directed=True)

    for line in inputs.splitlines():
        if not line.strip():
            break

        wf = Workflow.from_line(line)
        workflows[wf.name] = wf
        for rule in wf.rules:
            graph.add_edge(wf.name, rule.destination)

    total = 0
    for destination in ACCEPTED_DESTINATIONS:
        for route in nx.all_simple_edge_paths(graph, "in", destination):
            values = {i: Range() for i in "xmas"}
            for source, dest in route:
                wf = workflows[source]

                for rule in wf.rules:
                    if rule.attrtibute is None:
                        continue

                    at_destination = rule.destination == dest

                    if rule.comparison == operator.gt:
                        if at_destination:
                            values[rule.attrtibute].set_min(rule.value + 1)
                        else:
                            values[rule.attrtibute].set_max(rule.value)
                    elif rule.comparison == operator.lt:
                        if at_destination:
                            values[rule.attrtibute].set_max(rule.value - 1)
                        else:
                            values[rule.attrtibute].set_min(rule.value)
                    else:
                        raise ValueError(f"Unknown comparison {rule.comparison}")

                    if at_destination:
                        break

            this_values = 1
            for a, r in values.items():
                this_values *= r.num_values()
            total += this_values

    return total
