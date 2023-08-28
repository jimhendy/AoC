import os
import re

import networkx as nx


def run(inputs):
    g = nx.DiGraph()
    reg = re.compile(r"(\w+)")
    for row in inputs.split(os.linesep):
        parent, weight, *children = reg.findall(row)
        g.add_node(parent)
        for c in children:
            print(parent, c)
            g.add_edge(parent, c)

    # Start from a "random" node (last one) and find all predecssors
    n = parent
    while True:
        preds = list(g.predecessors(n))
        if not len(preds):
            return n
        n = preds[0]
