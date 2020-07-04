import os
import numpy as np

def run(inputs):
    return np.sum(np.ptp(np.array([np.array(i.split('\t')) for i in inputs.split('\n')]).astype(int), axis=1))