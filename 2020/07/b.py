import os
import re

import networkx as nx


def run(inputs):
    graph = nx.DiGraph()
    for line in inputs.split(os.linesep):
        parent = line.split("contain")[0].split("bags")[0].strip()
        if "no other bags" in line:
            graph.add_node(parent)
        else:
            children = re.findall(
                r"(\d+) ([\w\s]+) bag(?:s)?(?:[\.\,])?",
                line.split("contain")[1],
            )
            [graph.add_edge(parent, c[1], weight=int(c[0])) for c in children]

    queue = ["shiny gold"]
    total = 0

    while queue:
        considered = queue.pop()
        total += 1
        [
            queue.append(sub_bag)
            for sub_bag in graph[considered]
            for _ in range(graph[considered][sub_bag]["weight"])
        ]

    return total - 1  # Un-count the original shiny gold bag
