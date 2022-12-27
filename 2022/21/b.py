import operator
from typing import Dict, List, Tuple, Union

from tools.binary_search import binary_search

ROOT_MONKEY = "root"
ME_MONKEY = "humn"

ORIG_MONKIES: Dict[str, int] = {}

OPS = {
    "*": operator.mul,
    "/": operator.truediv,
    "+": operator.add,
    "-": operator.sub,
}
OP_MONKIES: List[Tuple[str, Union[int, Tuple[str, ...]]]] = []


def test(humn: int) -> bool:
    monkies = ORIG_MONKIES.copy()
    monkies[ME_MONKEY] = humn
    while ROOT_MONKEY not in monkies:
        for line in OP_MONKIES:
            name = line[0][:-1]
            if name in monkies or name == ME_MONKEY:
                continue
            depends_on = line[1], line[3]
            if all(d in monkies for d in depends_on):
                if name == ROOT_MONKEY:
                    print(humn)
                    print(monkies[depends_on[0]], monkies[depends_on[1]])
                    return monkies[depends_on[0]] >= monkies[depends_on[1]]
                else:
                    monkies[name] = OPS[line[2]](
                        monkies[depends_on[0]], monkies[depends_on[1]]
                    )


def run(inputs):
    global OP_MONKIES
    global ORIG_MONKIES

    inputs = [line.split() for line in inputs.splitlines()]

    # Load numbers
    ORIG_MONKIES = {line[0][:-1]: int(line[1]) for line in inputs if len(line) == 2}
    OP_MONKIES = [line for line in inputs if len(line) != 2]

    return binary_search(test)
