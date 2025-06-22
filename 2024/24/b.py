from dataclasses import dataclass, field
from typing import Literal


@dataclass
class Node:
    name: str
    value: int | None = None
    inputs: list[str] = field(default_factory=list)
    operation: Literal["AND", "OR", "XOR"] | None = None

    def __post_init__(self):
        if self.value is not None and (self.inputs or self.operation):
            raise ValueError(
                f"Node {self.name} cannot have both value and inputs/operation."
            )
        if self.value is None and (not self.inputs and not self.operation):
            raise ValueError(
                f"Node {self.name} must have either inputs or an operation defined."
            )

    def is_ready(self, nodes: "Nodes") -> bool:
        if self.value is not None:
            return True
        return all(
            nodes.get_node(input_name).is_ready(nodes) for input_name in self.inputs
        )

    def calculate(self, nodes: "Nodes") -> int:
        if not self.is_ready(nodes):
            raise ValueError(f"Node {self.name} is not ready for calculation.")

        if self.value is not None:
            return self.value

        input_values = [
            nodes.get_node(input_name).calculate(nodes) for input_name in self.inputs
        ]

        if self.operation == "AND":
            value = int(all(input_values))
        elif self.operation == "OR":
            value = int(any(input_values))
        elif self.operation == "XOR":
            value = int(sum(input_values) % 2 != 0)
        else:
            raise ValueError(
                f"Unknown operation {self.operation} for node {self.name}."
            )

        self.value = value
        return value

    def reset(self):
        if not self.inputs and not self.operation:
            return
        self.value = None


@dataclass
class Nodes:
    nodes: dict[str, Node] = field(default_factory=dict)

    def decimal(self, prefix: str) -> int:
        _nodes = {
            name: node for name, node in self.nodes.items() if name.startswith(prefix)
        }
        sorted_nodes = sorted(_nodes.items(), key=lambda item: item[0])
        result = 0
        for i, value in enumerate(sorted_nodes):
            result += value[1].value * 2**i
        return result

    def binary(self, prefix: str) -> list[int]:
        return self.decimal_to_binary(self.decimal(prefix))

    def get_node(self, name: str) -> Node:
        return self.nodes[name]

    def all_calculated(self) -> bool:
        return all(node.value is not None for node in self.nodes.values())

    def calculate_all(self):
        while not self.all_calculated():
            for node in self.nodes.values():
                if node.is_ready(self):
                    node.calculate(self)

    def add(self, node: Node):
        if node.name in self.nodes:
            raise ValueError(f"Node {node.name} already exists.")
        self.nodes[node.name] = node

    @staticmethod
    def binary_to_decimal(binary: list[int]) -> int:
        return sum(value * (2**i) for i, value in enumerate(reversed(binary)))

    @staticmethod
    def decimal_to_binary(decimal: int) -> list[int]:
        if decimal == 0:
            return [0]
        binary = []
        while decimal > 0:
            binary.append(decimal % 2)
            decimal //= 2
        return binary[::-1]

    def reset(self):
        for node in self.nodes.values():
            node.reset()

    def swap(self, name_a: str, name_b: str):
        a = self.get_node(name_a)
        b = self.get_node(name_b)

        a.name, b.name = b.name, a.name
        self.nodes[name_a], self.nodes[name_b] = self.nodes[name_b], self.nodes[name_a]


def run(inputs: str) -> int:
    nodes = Nodes()

    initial, calcs = inputs.split("\n\n")
    for line in initial.splitlines():
        name, value = line.split()
        name = name.rstrip(":")
        nodes.add(Node(name, value=int(value)))

    gate_outputs = []
    for line in calcs.splitlines():
        parts = line.split()
        nodes.add(
            Node(
                name=parts[-1],
                inputs=[parts[0], parts[2]],
                operation=parts[1],
            )
        )
        gate_outputs.append(parts[-1])

    pairs = [
        ("z39", "jct"),
        ("z21", "rcb"),
        ("z09", "gwh"),
        ("wgb", "wbw"),
    ]

    for a, b in pairs:
        nodes.swap(a, b)

    nodes.calculate_all()

    current = nodes.decimal("z")
    expected_result = nodes.decimal("x") + nodes.decimal("y")

    assert (
        current == expected_result
    ), "The calculated value does not match the expected value."

    return ",".join(i for p in pairs for i in p)
