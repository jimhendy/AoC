import numba
import numpy as np


@numba.njit
def n_presents(target):
    max_num = target // 10
    houses = np.zeros(max_num)
    for elf in range(1, max_num):
        # elf gives to their first house and in steps of that number
        houses[elf::elf] += 10 * elf
        pass
    return houses


def run(target):
    target = int(target)

    pres = n_presents(target)

    return np.min(np.argwhere(pres > target))
