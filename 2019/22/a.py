import os
import numba
import numpy as np


@numba.njit(numba.int64[:](numba.int64[:]))
def deal_into_new_stack(cards):
    return cards[::-1]


@numba.njit(numba.int64[:](numba.int64[:], numba.int64))
def deal_with_increment(cards, inc):
    out = cards.copy()
    j = 0
    for i in range(cards.shape[0]):
        out[j] = cards[i]
        j = (j + inc) % cards.shape[0]
        pass
    return out


def cut(cards, N):
    return np.roll(cards, -N)


def run(inputs):
    cards = np.array(range(10007))

    instructions = []
    for i in inputs.split(os.linesep):
        ins = "_".join(i.split())
        if ins[-1].isdigit():
            ins = "_".join(ins.split("_")[:-1]), int(ins.split("_")[-1])
            pass
        instructions.append(ins)
        pass

    for i in instructions:
        if type(i) == tuple:
            cards = globals()[i[0]](cards, *i[1:])
            pass
        else:
            cards = globals()[i](cards)
            pass
        pass

    return np.argwhere(cards == 2019)
