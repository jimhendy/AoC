import networkx as nx
import re


def run(inputs):
    connections = re.findall("(\d+) <-> ([\d, ]+)+", inputs)

    graph = nx.Graph()

    for c in connections:
        for dest in c[1].split(", "):
            graph.add_edge(c[0], dest)

    return len(nx.descendants(graph, "0")) + 1
