import os
import re

import numpy as np


def swap_position(s, x, y):
    x = int(x)
    y = int(y)
    letter_x = s[x]
    letter_y = s[y]
    s[x] = letter_y
    s[y] = letter_x
    return s


def swap_letter(s, x, y):
    mask_x = s == x
    mask_y = s == y
    s[mask_x] = y
    s[mask_y] = x
    return s


def rotate_left_right(s, lr, x):
    x = int(x)
    if lr == "right":
        return np.roll(s, x)
    else:
        return np.roll(s, -x)


def rotate_positions(s, x):
    pos_of_x = np.argwhere(s == x)[0]
    steps = 1 + pos_of_x
    if pos_of_x >= 4:
        steps += 1
    return np.roll(s, steps)


def reverse_positions(s, x, y):
    x = int(x)
    y = int(y)
    span = s[x : y + 1]
    s[x : y + 1] = span[::-1]
    return s


def move_position(s, x, y):
    x = int(x)
    y = int(y)
    value = s[x]
    s = np.delete(s, x)
    return np.insert(s, y, value)


def run(inputs):
    pswd = np.array(list("abcdefgh"))
    func_map = {
        re.compile(r"^swap position (\d+) with position (\d+)$"): swap_position,
        re.compile(r"^swap letter (\w) with letter (\w)$"): swap_letter,
        re.compile(r"^rotate (\w+) (\d+) steps?$"): rotate_left_right,
        re.compile(r"^rotate based on position of letter (\w)$"): rotate_positions,
        re.compile(r"^reverse positions (\w) through (\w)$"): reverse_positions,
        re.compile(r"^move position (\w) to position (\w)$"): move_position,
    }
    for ins in inputs.split(os.linesep):
        for reg, func in func_map.items():
            if reg.search(ins):
                pswd = func(pswd, *reg.findall(ins)[0])
                break
    return "".join(pswd)
