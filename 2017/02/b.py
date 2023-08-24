import numpy as np


def run(inputs):
    values = np.array([np.array(i.split("\t")) for i in inputs.split("\n")]).astype(int)
    output = 0
    for col in range(values.shape[1]):
        div = values / values[:, col][:, np.newaxis]
        output += np.sum(div[(div == div.astype(int)) & (div != 1)])
    return output
