import numba
import numpy as np


@numba.njit
def n_presents(target):
    pres_per_elf = 11
    max_num = target // pres_per_elf
    houses = np.zeros(max_num)
    for elf in range(1, max_num):
        # elf gives to their first house and in steps of that number
        houses[elf : elf * 50 + 1 : elf] += pres_per_elf * elf
    return houses


def run(target):
    target = int(target)

    pres = n_presents(target)

    return np.min(np.argwhere(pres > target))
