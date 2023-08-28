import os

import networkx as nx
import numpy as np

STEPS = np.array([np.array(i) for i in [(1, 0), (-1, 0), (0, 1), (0, -1)]])

import numba


@numba.njit(numba.boolean(numba.int64[:], numba.int64[:, :]))
def is_valid_pos(pos, layout):
    if not (0 < pos[0] < len(layout[0])):
        return False
    if not (0 < pos[1] < len(layout)):
        return False
    return True


def get_gates(layout):
    # Gates are defined as the period next to two adjacent uppercase letters
    data = {}
    for y, row in enumerate(layout):
        for x, char_o in enumerate(row):
            char = chr(char_o)
            if not char.isupper():
                continue
            pos = np.array([x, y])
            for step in STEPS:
                next_pos = pos + step
                if not is_valid_pos(next_pos, layout):
                    continue
                next_char = chr(get_char(next_pos, layout))
                if next_char.isupper():
                    next_next_pos = next_pos + step
                    if not is_valid_pos(next_next_pos, layout):
                        continue
                    next_next_char = chr(get_char(next_next_pos, layout))
                    if next_next_char == ".":
                        if step[1] == 1 or step[0] == 1:
                            key = f"{char}{next_char}"
                        else:
                            key = f"{next_char}{char}"
                            pass
                        if key in data:
                            key += "_1"
                        data[key] = next_next_pos
    return data


@numba.njit(numba.int64(numba.int64[:], numba.int64[:, :]))
def get_char(pos, layout):
    return layout[pos[1]][pos[0]]


@numba.njit(numba.boolean(numba.int64[:], numba.int64[:, :], numba.int64))
def set_char(pos, layout, char):
    if not is_valid_pos(pos, layout):
        return False
    layout[pos[1]][pos[0]] = char
    return True


@numba.njit(numba.int64(numba.int64[:], numba.int64[:], numba.int64[:, :]))
def dijkstra(origin, destination, layout_orig):
    layout = layout_orig.copy()
    layout_prev = layout.copy()
    seen_char = 48  # ord('0')
    origin_set = set_char(origin, layout_prev, seen_char)
    steps = 0
    if not origin_set:
        return -1
    while True:
        if get_char(destination, layout) == seen_char:
            return steps

        for y in range(layout_prev.shape[0]):
            row = layout_prev[y]
            for x in range(row.shape[0]):
                char = row[x]
                if char == seen_char:
                    pos = np.array([x, y])
                    for step_i in range(STEPS.shape[0]):
                        step = STEPS[step_i]
                        next_pos = pos + step
                        if not is_valid_pos(next_pos, layout):
                            continue
                        next_char = get_char(next_pos, layout_prev)
                        if next_char == 46:  # ord('.')
                            set_char(next_pos, layout, seen_char)
                            pass
                        pass
                    pass
                pass
            pass
        if np.array_equal(layout_prev, layout):
            return -1
        layout_prev = layout.copy()
        steps += 1
        pass
    pass
    return None


def plot(layout):
    [print("".join(map(chr, i))) for i in layout]
    print()


def run(inputs):
    layout = np.array([list(map(ord, i)) for i in inputs.split(os.linesep)])
    plot(layout)

    gates = get_gates(layout)
    graph = nx.Graph()

    [graph.add_node(k, pos=v) for k, v in gates.items()]

    for k in gates:
        if not k.endswith("_1"):
            continue
        graph.add_edge(k, k.replace("_1", ""), weight=1)
        pass

    for o_name, o in gates.items():
        for d_name, d in gates.items():
            if graph.has_edge(o_name, d_name):
                continue
            distance = dijkstra(o, d, layout)
            if distance < 0:
                continue
            graph.add_edge(o_name, d_name, weight=distance)
            pass
        pass
    """
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw(graph, pos)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    nx.draw_networkx_labels(graph, pos)
    plt.show()
    """
    return nx.dijkstra_path_length(graph, "AA", "ZZ")
