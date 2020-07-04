import os
import re
import numpy as np
import networkx as nx
from functools import lru_cache

@lru_cache(2048)
def total_weight(node, graph):
    total = nx.get_node_attributes(graph, 'weight')[node]
    for s in graph.successors(node):
        total += total_weight(s, graph)
    return total

def run(inputs):
    g = nx.DiGraph()
    reg = re.compile('(\w+)')
    for row in inputs.split(os.linesep):
        parent, weight, *children = reg.findall(row)
        g.add_node(parent, weight=int(weight))
        for c in children:
            print(parent, c)
            g.add_edge(parent, c)

    # Start from a "random" node (last one) and find all predecssors
    n = parent
    while True:
        preds = [i for i in g.predecessors(n)]
        if not len(preds):
            break
        n = preds[0]

    # n is now the root node
    prev_good_weight = None
    while True:
        successors = [i for i in g.successors(n)]
        suc_w = {
            s : total_weight(s, g)
            for s in successors
        }
        median = np.median(list(suc_w.values()))
        bad_node = [k for k,v in suc_w.items() if v != median]
        
        if not len(bad_node):
            # n  is the node with the incorrect weight
            return nx.get_node_attributes(g,'weight')[n] - (total_weight(n, g) - prev_good_weight)
        prev_good_weight = median
        n = bad_node[0]
    