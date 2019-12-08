import numpy as np


def floating_weights(weights):
    return np.array(weights.split()).astype(float)


def calculate_fuel(weights):
    return np.clip(
        np.subtract(
            np.floor(
                np.divide(weights, 3)
            ),
            2
        ),
        a_min=0, a_max=np.inf
    )
