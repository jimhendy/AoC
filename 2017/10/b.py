import re
import numpy as np


def run(inputs):
    n_elements = 256

    lengths_suffix = list(map(int, "17, 31, 73, 47, 23".split(",")))

    lengths = list(map(ord, inputs))
    lengths.extend(lengths_suffix)

    n_rounds = 64

    List = np.arange(n_elements)

    current_position = 0
    skip_size = 0

    for round in range(n_rounds):
        for length in lengths:
            r_list = np.roll(List, -current_position)
            sub_list = r_list[:length]
            r_list[:length] = sub_list[::-1]
            List = np.roll(r_list, +current_position)

            current_position += length + skip_size
            current_position %= len(List)
            skip_size += 1

    dense_hash = [np.bitwise_xor.reduce(List[i * 16 : (i + 1) * 16]) for i in range(16)]

    knot_hash = "".join([re.sub("^0x", "", hex(i)).zfill(2) for i in dense_hash])

    return knot_hash
