import re

import numba


@numba.njit
def rand(seed):
    return (seed * 252533) % 33554393


@numba.njit
def find_rand(prev, desired_i):
    i = 1
    while True:
        prev = rand(prev)
        i += 1
        if i >= desired_i:
            return prev


def index_from_row_col(row, col):
    return sum(range(row + col - 1)) + col


def run(inputs):
    aim_row = int(re.findall(r"row (\d+)", inputs)[0])
    aim_col = int(re.findall(r"column (\d+)", inputs)[0])

    desired_i = index_from_row_col(aim_row, aim_col)

    prev = 20151125
    return find_rand(prev, desired_i)
