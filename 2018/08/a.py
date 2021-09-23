from node import Node


def sum_metadata(node):
    total = sum(node.metadata)
    for c in node.children:
        total += sum_metadata(c)
    return total


def run(inputs):
    int_inputs = list(map(int, inputs.split()))
    node = Node(int_inputs)
    return sum_metadata(node)
