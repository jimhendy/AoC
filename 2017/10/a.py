import numpy as np

def run(inputs):
    n_elements = 256
    List = np.arange(n_elements)
    
    current_position = 0
    skip_size = 0

    for length in map(int, inputs.split(',')):
        r_list = np.roll(List, -current_position)
        sub_list = r_list[:length]
        r_list[:length] = sub_list[::-1]
        List = np.roll(r_list, +current_position)

        current_position += length + skip_size
        current_position %= len(List)
        skip_size += 1

    return np.prod(List[:2])