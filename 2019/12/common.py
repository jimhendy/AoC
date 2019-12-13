import os
import numpy as np


def apply_gravity(m1, m2):
    delta = np.sign(m1.position - m2.position)
    m1.update_velocity(np.multiply(-1, delta))
    m2.update_velocity(delta)
    pass
