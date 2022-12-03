import re

import optcode
import pandas as pd


def run(inputs):
    reg = re.compile(
        r"Before:\s+\[([\s\,\-\d]+)\]\s([\-\d\s]+)\sAfter:\s+\[([\s\,\-\d]+)\]"
    )
    funcs = [
        "addr",
        "addi",
        "mulr",
        "muli",
        "banr",
        "bani",
        "borr",
        "bori",
        "setr",
        "seti",
        "gtir",
        "gtri",
        "gtrr",
        "eqir",
        "eqri",
        "eqrr",
    ]

    df = pd.DataFrame(True, columns=funcs, index=range(16))
    oc = optcode.OptCode([])

    total = 0

    for match in reg.findall(inputs):
        before = list(map(int, match[0].split(",")))
        after = list(map(int, match[2].split(",")))
        params = list(map(int, match[1].split()))
        possibles = 0
        for f in funcs:
            func = getattr(oc, f)
            oc.registers = before[:]
            func(*params[1:])
            if oc.registers == after:
                possibles += 1
            else:
                df.loc[params[0], f] = False
        if possibles >= 3:
            total += 1

    mapping = {}
    while len(mapping) != len(funcs):
        for col in df.columns:
            if df[col].sum() == 1:
                value = df[col].idxmax()
                mapping[value] = col
                df = df[df.index != value]

    for k in sorted(list(mapping.keys())):
        print(f'{k}: "{mapping[k]}"')

    return total
