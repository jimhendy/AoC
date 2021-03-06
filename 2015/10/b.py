import tqdm
import itertools


def evaluate(num):
    return ''.join([str(len(list(g))) + str(k) for k, g in itertools.groupby(num)])


def run(inputs):

    num = str(int(inputs))
    for _ in tqdm.tqdm(range(50)):
        num = evaluate(num)
        pass
    return len(str(num))
