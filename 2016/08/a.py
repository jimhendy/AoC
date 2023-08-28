import os
import re

import numpy as np
import seaborn as sns

N_COLS = 50
N_ROWS = 6


def rect(pixels, A, B):
    for x in range(A):
        for y in range(B):
            pixels[y][x] = 1


def rotate_row(pixels, A, B):
    pixels[A] = np.roll(pixels[A], B)


def rotate_col(pixels, A, B):
    pixels[:, A] = np.roll(pixels[:, A], B)


REGS = {
    rect: re.compile(r"^rect (\d+)x(\d+)$"),
    rotate_row: re.compile(r"^rotate row y=(\d+) by (\d+)$"),
    rotate_col: re.compile(r"^rotate column x\=(\d+) by (\d+)$"),
}


def run(inputs):
    pixels = np.array([0] * N_ROWS * N_COLS).reshape(N_ROWS, -1)

    for ins in inputs.split(os.linesep):
        found_ins = False
        for func, reg in REGS.items():
            for match in reg.findall(ins):
                func(pixels, *map(int, match))
                found_ins = True

            if found_ins:
                break
        if found_ins:
            continue
        raise Exception(ins)

    sns.heatmap(pixels)

    return pixels.sum()
