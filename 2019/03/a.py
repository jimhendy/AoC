import common
import numpy as np


def run(inputs):

    wire_coords = common.get_wire_coords(inputs)

    intersections = common.get_intersections(
        wire_coords
    )
    int_distances = np.abs(intersections).sum(axis=1)
    min_distance = min([d for d in int_distances if d != 0])
    return min_distance
