import pandas as pd


class Node:
    def __init__(self, line) -> None:
        parts = line.split()
        self._inputs = [parts[0], parts[2]]
        self.output = parts[-1]
        self.original_output = self.output
        self.operation = parts[1]

    @property
    def input_a(self) -> str:
        return sorted(self._inputs)[0]

    @property
    def input_b(self) -> str:
        return sorted(self._inputs)[1]

    def number(self) -> str:
        """Return the number of the output node."""
        if self.input_a.startswith("x"):
            return self.input_a[1:]
        raise ValueError(f"Unsupported operation: {self.operation}")

    def to_dict(self) -> dict:
        return {
            "input_a": self.input_a,
            "input_b": self.input_b,
            "output": self.output,
            "operation": self.operation,
            "original_output": self.original_output,
        }

    def replace_input(self, original_name: str, new_name: str) -> None:
        for i, input_ in enumerate(self._inputs):
            if input_ == original_name:
                self._inputs[i] = new_name


def rename(operation: str, prefix: str, nodes: list[Node]) -> None:
    for node in nodes:
        if (
            node.operation == operation
            and node.input_a.startswith("x")
            and not node.output.startswith("z")
        ):
            number = node.number()
            new_node = f"{prefix}{number}"
            old_node = node.output
            node.output = new_node
            for n in nodes:
                n.replace_input(old_node, new_node)


def run(inputs: str) -> int:
    initial, calcs = inputs.split("\n\n")
    nodes = []
    for line in calcs.splitlines():
        nodes.append(Node(line))

    rename("XOR", "a", nodes)
    rename("AND", "b", nodes)

    df = (
        pd.DataFrame([node.to_dict() for node in nodes])
        .sort_values(["operation", "input_a", "input_b"])
        .reset_index(drop=True)
    )

    df.to_csv("nodes.csv", index=False)

    return 1
