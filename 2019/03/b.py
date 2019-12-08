import common
import numpy as np


def run(inputs):

    wire_coords = common.get_wire_coords(inputs)

    intersections = common.get_intersections(
        wire_coords
    )

    indices = np.array([
        [
            common.index_of_array(wire_coords[0], i),
            common.index_of_array(wire_coords[1], i)
        ]
        for i in intersections
    ])

    min_steps = indices.sum(axis=1)
    min_steps = [i for i in min_steps if i != 0]
    min_steps = min(min_steps)

    return min_steps
