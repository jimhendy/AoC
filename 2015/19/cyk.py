from collections import defaultdict


def _get_combs(y, x, data):
    if y == 0:
        yield from data[y][x]
    for yi in range(y):  # 0 -> (y-1)
        new_base = data[yi][x]
        for b in new_base:
            for other in _get_combs(y - 1 - yi, x + yi + 1, data):
                yield f"{b}{other}"


def cyk(target, grammar):
    """
    Target : str, the string we wish to test if it is in the language
    grammar: dict, key of root, values as list of strings.
    """
    # x is (y,x) dict of strings
    data = defaultdict(lambda: defaultdict(set))

    possibles = {i for j in grammar.values() for i in j}

    # First time is special
    for i in range(len(target)):
        data[0][i] = {target[i]}

    for y in range(1, len(target) + 1):
        for x in range(len(target) - y):
            for this_target in _get_combs(y, x, data):
                if this_target not in possibles:
                    continue
                for k, v in grammar.items():
                    print(this_target)
                    if this_target in v:
                        data[y][x].add(k)

    for k, v in data.items():
        out = "".join([str(i) for i in v.values() if len(i)])
        if len(out):
            print(k, out)

    return data
