import networkx as nx


def run(inputs: str) -> str:
    G = nx.Graph()
    for line in inputs.splitlines():
        a, b = line.split("-")
        G.add_edge(a, b)

    max_clique = []
    for clique in nx.find_cliques(G):
        if len(clique) > len(max_clique):
            max_clique = clique

    return ",".join(sorted(max_clique))
