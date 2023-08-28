import operator

ROOT_MONKEY = "root"


def run(inputs):
    inputs = [line.split() for line in inputs.splitlines()]

    # Load numbers
    monkies = {line[0][:-1]: int(line[1]) for line in inputs if len(line) == 2}

    ops = {
        "*": operator.mul,
        "/": operator.truediv,
        "+": operator.add,
        "-": operator.sub,
    }

    while ROOT_MONKEY not in monkies:
        for line in inputs:
            if len(line) == 2:
                continue
            name = line[0][:-1]
            if name in monkies:
                continue
            depends_on = line[1], line[3]
            if all(d in monkies for d in depends_on):
                monkies[name] = ops[line[2]](
                    monkies[depends_on[0]],
                    monkies[depends_on[1]],
                )

    return monkies[ROOT_MONKEY]
