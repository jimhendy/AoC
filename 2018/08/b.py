from node import Node

def run(inputs):
    int_inputs = list(map(int, inputs.split()))
    node = Node(int_inputs)
    return node.value()