import itertools
import os
import re

import networkx as nx


def run(inputs):

    reg = re.compile("(.+) to (.+) = (\d+)")

    graph = nx.Graph()

    for line in inputs.split(os.linesep):
        matches = reg.findall(line)[0]
        graph.add_edge(matches[0], matches[1], weight=int(matches[2]))
        pass

    best_path_length = None
    for path in itertools.permutations(graph.nodes):

        this_path_length = 0

        for i, j in zip(path[:-1], path[1:]):
            this_path_length += graph[i][j]["weight"]

        if best_path_length is None or this_path_length > best_path_length:
            best_path_length = this_path_length
            # print(best_path_length, path)
            pass

        pass

    return best_path_length
