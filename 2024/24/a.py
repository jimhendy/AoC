from dataclasses import dataclass, field
from typing import Literal

NODES = {}


@dataclass
class Node:
    name: str
    value: int | None = None
    inputs: list[str] = field(default_factory=list)
    operation: Literal["AND", "OR", "XOR"] | None = None

    def __post_init__(self):
        if self.value is not None and (self.inputs or self.operation):
            raise ValueError(
                f"Node {self.name} cannot have both value and inputs/operation.",
            )
        if self.value is None and (not self.inputs and not self.operation):
            raise ValueError(
                f"Node {self.name} must have either inputs or an operation defined.",
            )

    def is_ready(self) -> bool:
        if self.value is not None:
            return True
        return all(NODES[input_name].is_ready() for input_name in self.inputs)

    def calculate(self) -> int:
        if not self.is_ready():
            raise ValueError(f"Node {self.name} is not ready for calculation.")

        if self.value is not None:
            return self.value

        input_values = [NODES[input_name].calculate() for input_name in self.inputs]

        if self.operation == "AND":
            value = int(all(input_values))
        elif self.operation == "OR":
            value = int(any(input_values))
        elif self.operation == "XOR":
            value = int(sum(input_values) % 2 != 0)
        else:
            raise ValueError(
                f"Unknown operation {self.operation} for node {self.name}.",
            )

        self.value = value
        return value


def run(inputs: str) -> int:
    initial, calcs = inputs.split("\n\n")
    for line in initial.splitlines():
        name, value = line.split()
        name = name.rstrip(":")
        NODES[name] = Node(name, value=int(value))

    for line in calcs.splitlines():
        parts = line.split()
        NODES[parts[-1]] = Node(
            name=parts[-1],
            inputs=[parts[0], parts[2]],
            operation=parts[1],
        )

    while any(node.value is None for node in NODES.values()):
        for node in NODES.values():
            if node.is_ready():
                node.calculate()

    z_nodes = {name: node.value for name, node in NODES.items() if name.startswith("z")}
    sorted_z_nodes = sorted(z_nodes.items(), key=lambda item: item[0])

    result = 0

    for i, value in enumerate(sorted_z_nodes):
        result += value[1] * 2**i

    return result
