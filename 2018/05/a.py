def run(inputs):
    polymer = list(inputs)
    swapped = list(inputs.swapcase())

    reduced = []
    for p, s in zip(polymer, swapped):
        if len(reduced) and reduced[-1] == s:
            reduced.pop()
        else:
            reduced.append(p)

    return len(reduced)
