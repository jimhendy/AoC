import os
from collections.abc import Callable

import numpy as np

from tools.number_conversion import binary_to_decimal


def find_value(inputs: np.ndarray, desired_bit_lambda: Callable) -> int:
    """
    Extract the last remaining row from ``inputs`` when iteratively filtering
    by ``desired_bit_lambda`` from the most-significant-bit to the least.

    :param inputs: Numpy array of binary values to filter.
    :param desired_bit_lambda: Lambda to filter the counts dict and extract \
        the desired bit value.
    :return: Integer of the decimal representation of the extracted binary value.
    """
    possibles = inputs.copy()
    bit_num = 0
    while possibles.shape[0] > 1:
        bits = possibles[:, bit_num]
        counts = dict(zip(*np.unique(bits, return_counts=True), strict=False))
        desired_bit = desired_bit_lambda(counts)
        possibles = possibles[bits == desired_bit]
        bit_num += 1
    return binary_to_decimal(possibles[0])


def run(inputs):
    inputs = np.array([list(i) for i in inputs.split(os.linesep)]).astype(int)

    ox = find_value(inputs, lambda x: 0 if x.get(0, 0) > x.get(1, 0) else 1)
    co2 = find_value(inputs, lambda x: 1 if x.get(0, 0) > x.get(1, 0) else 0)

    return ox * co2
