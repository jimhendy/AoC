import itertools

import tqdm


def evaluate(num):
    return "".join([str(len(list(g))) + str(k) for k, g in itertools.groupby(num)])


def run(inputs):
    num = str(int(inputs))
    for _ in tqdm.tqdm(range(50)):
        num = evaluate(num)
    return len(str(num))
