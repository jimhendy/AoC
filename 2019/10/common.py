import os

import numpy as np
import pandas as pd


def in_to_array(inputs):
    data = []
    for y, row in enumerate(inputs.split(os.linesep)):
        for x, cell in enumerate(row):
            if cell != "#":
                continue
            data.append([x, y])
    return np.array(data)


def num_visible(data):
    visible = {}
    for position in data:
        angle = _get_angle(data, position)
        visible[(position[0], position[1])] = len(np.unique(angle))
    return pd.Series(visible).sort_values()


def _get_angle(data, pos):
    delta = data - pos
    angle_ = (np.arctan2(-1 * delta[:, 1], delta[:, 0]) - np.pi / 2) * -1
    return (angle_ + 2 * np.pi) % (2 * np.pi)


def _get_distance(data, pos):
    delta = data - pos
    return np.sqrt(np.power(delta[:, 0], 2) + np.power(delta[:, 1], 2))
