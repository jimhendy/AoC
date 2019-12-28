import os
import re
import numpy as np
import networkx as nx
import matplotlib.pylab as plt
from collections import defaultdict

STEPS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

import numba

@numba.njit
def is_valid_pos(pos: , layout):
    if not (0 < pos[0] < len(layout[0])):
        return False
    if not (0 < pos[1] < len(layout)):
        return False
    return True

@numba.njit
def step_pos(pos, step):
    return (pos[0]+step[0], pos[1]+step[1])

#@numba.njit
def stepped_char(pos, step, layout):
    # Return the character in the stepped position
    # If the stepped pos is invalid, return a wall
    new_pos = step_pos(pos, step)
    if not is_valid_pos(new_pos, layout):
        return '#'
    return get_char(new_pos, layout)


def get_gates(layout):
    # Gates are defined as the period next to two adjacent uppercase letters
    data = {}
    for y, row in enumerate(layout):
        for x, char in enumerate(row):
            if not char.isupper():
                continue
            for step in STEPS:
                next_char = stepped_char((x, y), step, layout)
                if next_char.isupper():
                    if stepped_char((x, y), (2*step[0], 2*step[1]), layout) == '.':
                        if step[1] == 1 or step[0] == 1:
                            key = f'{char}{next_char}'
                        else:
                            key = f'{next_char}{char}'
                            pass
                        if key in data.keys():
                            key += '_1'
                        data[key] = (x + 2 * step[0], y + 2 * step[1])
    return data

@numba.njit
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

    layout = np.array([list(i) for i in inputs.split(os.linesep)])
    plot(layout)

    gates = get_gates(layout)
    graph = nx.Graph()
    
    [graph.add_node(k, pos=v) for k, v in gates.items()]

    for k,v in gates.items():
        if not k.endswith('_1'):
            continue
        graph.add_edge(k, k.replace('_1',''), weight=1)
        pass
    
    for o_name, o in gates.items():
        for d_name, d in gates.items():
            if graph.has_edge(o_name, d_name):
                continue
            distance = dijkstra(o, d, layout)
            if distance == False:
                continue
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
    distance = nx.dijkstra_path_length(graph, 'AA', 'ZZ')

    return distance
