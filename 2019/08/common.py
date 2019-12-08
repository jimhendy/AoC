import numpy as np

def in_to_array(inputs, n_rows=6, n_cols=25):
    data = np.array(list(inputs))
    return data.reshape(
        -1, n_rows, n_cols ).astype(int)
