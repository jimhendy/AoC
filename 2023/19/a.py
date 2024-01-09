import operator
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Part:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_line(cls, line: str) -> "Part":
        x, m, a, s = (x.split("=")[1] for x in line[1:-1].split(","))
        return cls(
            x=int(x),
            m=int(m),
            a=int(a),
            s=int(s),
        )

    @property
    def total(self):
        return self.x + self.m + self.a + self.s


@dataclass(frozen=True, slots=True)
class Rule:
    destination: str
    attrtibute: str | None = None
    comparison: operator.attrgetter | None = None
    value: int | None = None

    @classmethod
    def from_str(cls, line: str) -> "Rule":
        if ":" not in line:
            return cls(destination=line.strip())
        condition, destination = line.split(":")

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

    def evaluate(self, part: Part) -> str | None:
        if self.attrtibute is None:
            return self.destination
        if self.comparison(part.__getattribute__(self.attrtibute), self.value):
            return self.destination


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

    def evaluate(self, part: Part) -> bool:
        for rule in self.rules:
            if destination := rule.evaluate(part):
                return destination
        raise ValueError(f"Could not evaluate {self.name} for {part}")


def run(inputs: str) -> int:
    workflows = {}
    lines = inputs.splitlines()

    total = 0
    in_parts = False

    for line in lines:
        if not line.strip():
            in_parts = True
            continue

        if in_parts:
            part = Part.from_line(line)
            wf_name = "in"
            while wf_name not in ["R", "A"]:
                wf_name = workflows[wf_name].evaluate(part)
                if wf_name == "A":
                    total += part.total
        else:
            wf = Workflow.from_line(line)
            workflows[wf.name] = wf

    return total
