import os

import numpy as np


def index_of_array(array, value):
    return np.flatnonzero((array == value).all(1))[0]


def get_intersections(wire_coords):
    return np.array(
        list({tuple(x) for x in wire_coords[0]} & {tuple(x) for x in wire_coords[1]}),
    )


def get_wire_coords(inputs):
    wire_vertices = [w.split(",") for w in inputs.split(os.linesep)]
    wire_coords = []

    for wire_num, wv in enumerate(wire_vertices):
        previous_pos = np.array([0, 0])
        wire_coords.append([previous_pos])
        for v in wv:
            direction = v[0]
            step = int(v[1:])
            move_func = get_move_func(direction)
            for _s in range(step):
                previous_pos = move_func(previous_pos)
                wire_coords[wire_num].append(previous_pos)
    return wire_coords


def get_move_func(direction):
    step = {
        "U": np.array([1, 0]),
        "D": np.array([-1, 0]),
        "R": np.array([0, 1]),
        "L": np.array([0, -1]),
    }.get(direction)

    def f(p):
        return p + step

    return f
