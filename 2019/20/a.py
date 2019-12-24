import os
import re
import numpy as np
import networkx as nx
import matplotlib.pylab as plt
from collections import defaultdict

STEPS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def is_valid_pos(pos, layout):
    if not (0 < pos[0] < len(layout[0])):
        return False
    if not (0 < pos[1] < len(layout)):
        return False
    return True


def step_pos(pos, step):
    return (pos[0]+step[0], pos[1]+step[1])


def stepped_char(pos, step, layout):
    # Return the character in the stepped position
    # If the stepped pos is invalid, return a wall
    new_pos = step_pos(pos, step)
    if not is_valid_pos(new_pos, layout):
        return '#'
    return get_char(new_pos, layout)


def get_gates(layout):
    # Gates are defined as the period next to two adjacent uppercase letters
    data = defaultdict(list)
    for y, row in enumerate(layout):
        for x, char in enumerate(row):
            if not char.isupper():
                continue
            for step in STEPS:
                next_char = stepped_char((x, y), step, layout)
                if next_char.isupper():
                    if stepped_char((x, y), (2*step[0], 2*step[1]), layout) == '.':
                        data[''.join(sorted([char, next_char]))].append(
                            (x + 2 * step[0], y + 2 * step[1])
                        )
    return data


def get_char(pos, layout):
    if not is_valid_pos(pos, layout):
        return False
    return layout[pos[1]][pos[0]]


def set_char(pos, layout, char):
    if not is_valid_pos(pos, layout):
        return False
    layout[pos[1]][pos[0]] = char
    return True


def dijkstra(origin, destination, layout_orig):
    layout = np.array(layout_orig)
    layout_prev = layout.copy()
    seen_char = '0'
    origin_set = set_char(origin, layout_prev, seen_char)
    steps = 0
    if not origin_set:
        raise Exception(f'Canno\'t set origin at position {origin}')
    while True:
        if get_char(destination, layout) == seen_char:
            return steps

        for y, row in enumerate(layout_prev):
            for x, char in enumerate(row):
                if char == seen_char:
                    for step in STEPS:
                        next_char = stepped_char((x, y), step, layout_prev)
                        if next_char == '.':
                            set_char(step_pos((x, y), step), layout, seen_char)
                            pass
                        pass
                    pass
                pass
            pass
        # plot(layout)
        if np.array_equal(layout_prev, layout):
            print(f'Canno\'t find a path from {origin} to {destination}')
            return False
        layout_prev = layout.copy()
        steps += 1
    pass


def plot(layout):
    [print(''.join(i)) for i in layout]
    print()


def run(inputs):

    layout = [list(i) for i in inputs.split(os.linesep)]
    plot(layout)

    gates = get_gates(layout)
    graph = nx.Graph()

    [ graph.add_node(k, pos=v[0]) for k,v in gates.items() ]
    
    for o_name, o in gates.items():
        for d_name, d in gates.items():
            distances = [
                dijkstra(o_i, d_i, layout)
                for o_i in o
                for d_i in d
            ]
            distances = [ d for d in distances if d != False ]
            if not len(distances):
                continue
            distance = min(distances)
            graph.add_edge(o_name, d_name, weight=distance)
            pass
        pass
    '''
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw(graph, pos)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    nx.draw_networkx_labels(graph, pos)
    plt.show()
    '''

    sp = nx.dijkstra_path(graph, 'AA', 'ZZ')
    distance = nx.dijkstra_path_length( graph, 'AA', 'ZZ' )
    distance += len(sp) - 2

    return distance
