import os
import re
import networkx as nx

def run(inputs):
    graph = nx.DiGraph()
    for line in inputs.split(os.linesep):
        parent = line.split('contain')[0].split('bags')[0].strip()
        if 'no other bags' in line:
            graph.add_node(parent)
            continue
            
        children = re.findall(r'(\d+) ([\w\s]+) bag(?:s)?(?:[\.\,])?', line.split('contain')[1])
        [ graph.add_edge(parent, c[1], weight=int(c[0])) for c in children ]

    queue = ['shiny gold']
    possibles = set()

    while len(queue):
        considered = queue.pop()
        for p in graph.predecessors(considered):
            if p not in possibles:
                possibles.add(p)
                queue.append(p)

    return len(possibles)
