def run(inputs):
    drops = set(inputs.splitlines())
    total = 0
    for d in drops:
        total += 6
        loc = list(map(int, d.split(",")))
        for pos in range(len(loc)):
            for diff in [-1, +1]:
                neighbour = ",".join(
                    map(
                        str, [(v if i != pos else v + diff) for i, v in enumerate(loc)],
                    ),
                )
                if neighbour in drops:
                    total -= 1
    return total
