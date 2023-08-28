import os


def run(inputs):
    p1, p2 = (
        list(map(int, i.split(os.linesep)[1:])) for i in inputs.split(os.linesep * 2)
    )

    while p1 and p2:
        c1, c2 = p1.pop(0), p2.pop(0)
        if c1 > c2:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)

    p1.extend(p2)

    return sum([(i + 1) * j for i, j in enumerate(p1[::-1])])
