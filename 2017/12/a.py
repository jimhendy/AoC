import re

import networkx as nx


def run(inputs):
    connections = re.findall(r"(\d+) <-> ([\d, ]+)+", inputs)

    graph = nx.Graph()

    for c in connections:
        for dest in c[1].split(", "):
            graph.add_edge(c[0], dest)

    return len(nx.descendants(graph, "0")) + 1
