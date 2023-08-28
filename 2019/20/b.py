import copy
import heapq
import os

import networkx as nx
import numba
import numpy as np

STEPS = np.array([np.array(i) for i in [(1, 0), (-1, 0), (0, 1), (0, -1)]]).astype(
    np.int8,
)


@numba.njit(numba.boolean(numba.int8[:], numba.int8[:, :]))
def is_valid_pos(pos, layout):
    if (pos[0] < 0) or (pos[0] >= layout.shape[1]):
        return False
    if (pos[1] < 0) or (pos[1] >= layout.shape[0]):
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
            pos = np.array([x, y]).astype(np.int8)
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

                        if (
                            (pos[0] == 0)
                            or (pos[0] == layout.shape[1] - 1)
                            or (pos[1] == 0)
                            or (pos[1] == layout.shape[0] - 1)
                        ):
                            key += "_o"

                        else:
                            key += "_i"
                            pass

                        if key in data:
                            key += "_1"
                        data[key] = next_next_pos
    return data


@numba.njit(numba.int8(numba.int8[:], numba.int8[:, :]))
def get_char(pos, layout):
    return layout[pos[1]][pos[0]]


@numba.njit(numba.boolean(numba.int8[:], numba.int8[:, :], numba.int8))
def set_char(pos, layout, char):
    if not is_valid_pos(pos, layout):
        return False
    layout[pos[1]][pos[0]] = char
    return True


@numba.njit(numba.int8(numba.int8[:], numba.int8[:], numba.int8[:, :]))
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
                    pos = np.array([x, y]).astype(np.int8)
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
    layout = np.array([list(map(ord, i)) for i in inputs.split(os.linesep)]).astype(
        np.int8,
    )
    plot(layout)

    gates = get_gates(layout)
    graph = nx.Graph()

    [graph.add_node(k, pos=v) for k, v in gates.items()]

    for k in gates:
        if not k.endswith("_i"):
            continue
        graph.add_edge(k, k.replace("_i", "_o"), weight=1)
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

    # Steps, Path as (Location, Level)
    q = [(0, [("AA_o", 0)])]

    while q:
        steps, path = heapq.heappop(q)

        c_node = path[-1][0]
        c_level = path[-1][1]

        if c_node == "ZZ_o":
            if c_level == 0:
                for p in path:
                    print(p)
                    pass
                return steps
            continue
            pass

        for n in graph.neighbors(c_node):
            if n == "AA_o":
                continue

            if len(path) > 2 and path[-2][0] == n:
                continue

            new_path = copy.deepcopy(path)
            new_loc = (n, c_level)
            if new_loc in path:
                continue
            new_path.append(new_loc)
            new_steps = graph[c_node][n]["weight"]

            # If this is a gate, use it
            if n.endswith("_o") and n.replace("_o", "_i") in graph.neighbors(n):
                new_steps += 1
                if c_level == 0:
                    continue
                new_path.append((n.replace("_o", "_i"), c_level - 1))
                pass
            elif n.endswith("_i") and n.replace("_i", "_o") in graph.neighbors(n):
                new_path.append((n.replace("_i", "_o"), c_level + 1))
                new_steps += 1
                pass

            heapq.heappush(q, (steps + new_steps, new_path))
    return None
