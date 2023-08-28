import re

import networkx as nx


def run(inputs):
    connections = re.findall(r"(\d+) <-> ([\d, ]+)+", inputs)

    graph = nx.Graph()

    nodes = set()
    connected_nodes = set()

    for c in connections:
        nodes.add(c[0])
        for dest in c[1].split(", "):
            graph.add_edge(c[0], dest)

    n_groups = 0
    for n in nodes:
        if n in connected_nodes:
            continue
        n_groups += 1
        this_group = nx.descendants(graph, n)
        [connected_nodes.add(i) for i in this_group]
        connected_nodes.add(n)

    return n_groups
