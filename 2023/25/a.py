from functools import reduce

import networkx as nx


def run(inputs: str) -> int:
    graph = nx.Graph()
    for line in inputs.splitlines():
        from_, to_list = line.split(":")
        for to in to_list.split():
            graph.add_edge(from_, to)

    graph.remove_edges_from(nx.minimum_edge_cut(graph))
    if nx.is_connected(graph):
        raise ValueError("Graph is still connected")

    subgraphs = list(nx.connected_components(graph))
    return reduce(lambda x, y: x * y, map(len, subgraphs))
