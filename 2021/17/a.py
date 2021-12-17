import numpy as np


def run(inputs):
    y_lower = np.abs(-int(inputs.split("y=")[1].split("..")[0]))
    return y_lower * (y_lower-1) // 2
