import os
import numpy as np
from scipy.stats import mode
from tools.binary_nums import binary_to_decimal


def run(inputs):
    inputs = np.array([list(i) for i in inputs.split(os.linesep)]).astype(int)
    gamma_bin = mode(inputs)[0][0]

    gamma = binary_to_decimal(gamma_bin)

    epsilon_bin = np.logical_not(gamma_bin).astype(int)
    epsilon = binary_to_decimal(epsilon_bin)

    return gamma * epsilon
