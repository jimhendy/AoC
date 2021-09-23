import networkx as nx
from point import Point

STEPS = {"E": Point(-1, 0), "W": Point(+1, 0), "N": Point(0, -1), "S": Point(0, +1)}


def run(inputs):

    inputs = inputs.strip().rstrip("$").lstrip("^")
    graph = nx.Graph()
    pos = Point(0, 0)
    before_brackets = []

    for c in inputs:
        if c == "(":
            before_brackets.append(pos)
        elif c in STEPS.keys():
            new_pos = pos + STEPS[c]
            graph.add_edge(pos, new_pos)
            pos = new_pos
        elif c == "|":
            pos = before_brackets[-1]
        elif c == ")":
            pos = before_brackets.pop()

    return len(
        [k for k, v in nx.shortest_path(graph, Point(0, 0)).items() if len(v) > 1_000]
    )
