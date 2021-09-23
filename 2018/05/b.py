def reduced_length(inputs, omit):
    omit = omit.lower()

    polymer = list(inputs)
    swapped = list(inputs.swapcase())
    lowercase = list(inputs.lower())

    reduced = []
    for p, s, l in zip(polymer, swapped, lowercase):
        if l == omit:
            continue
        if len(reduced) and reduced[-1] == s:
            reduced.pop()
        else:
            reduced.append(p)

    return len(reduced)


def run(inputs):
    possibles = set((i.lower() for i in list(inputs)))
    return min([reduced_length(inputs, p) for p in possibles])
