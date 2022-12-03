import os

import numba
import numpy as np


def deal_into_new_stack(n_cards, a, b):
    a *= -1
    b = (n_cards - 1) - b
    return a, b


def deal_with_increment(n_cards, a, b, inc):
    z = pow(inc, n_cards - 2, n_cards)  # == modinv(n,L)
    a = a * z % n_cards
    b = b * z % n_cards
    return a, b


def cut(n_cards, a, b, N):
    b = (b + N) % n_cards
    return a, b


def polypow(a, b, m, n):
    if m == 0:
        return 1, 0
    if m % 2 == 0:
        return polypow(a * a % n, (a * b + b) % n, m // 2, n)
    else:
        c, d = polypow(a, b, m - 1, n)
        return a * c % n, (a * d + b) % n


def run(inputs):

    n_cards = 119315717514047
    n_shuffles = 101741582076661
    pos = 2020

    instructions = []
    for i in inputs.split(os.linesep):
        ins = "_".join(i.split())
        if ins[-1].isdigit():
            ins = "_".join(ins.split("_")[:-1]), int(ins.split("_")[-1])
            pass
        instructions.append(ins)
        pass

    a = 1
    b = 0

    for i in instructions[::-1]:
        if type(i) == tuple:
            a, b = globals()[i[0]](n_cards, a, b, *i[1:])
            pass
        else:
            a, b = globals()[i](n_cards, a, b)
            pass
        pass

    a, b = polypow(a, b, n_shuffles, n_cards)

    result = (pos * a + b) % n_cards

    return result
