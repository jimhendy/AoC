import os


def repr_list(l):
    return ",".join(map(str, l))


def game(p1, p2):
    # Return p1_win, score

    cache = {"p1": set(), "p2": set()}

    while p1 and p2:
        p1_config, p2_config = repr_list(p1), repr_list(p2)
        if p1_config in cache["p1"] or p2_config in cache["p2"]:
            return True, None

        cache["p1"].add(p1_config)
        cache["p2"].add(p2_config)

        c1, c2 = p1.pop(0), p2.pop(0)
        if len(p1) >= c1 and len(p2) >= c2:
            p1_win, _ = game(p1[:c1], p2[:c2])
        else:
            p1_win = c1 > c2

        if p1_win:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)

    p1.extend(p2)
    result = not len(p2), sum([(i + 1) * j for i, j in enumerate(p1[::-1])])

    return result


def run(inputs):
    p1, p2 = [
        list(map(int, i.split(os.linesep)[1:])) for i in inputs.split(os.linesep * 2)
    ]
    return game(p1, p2)[1]
