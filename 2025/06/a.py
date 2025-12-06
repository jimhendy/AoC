import operator
from collections import defaultdict
from functools import reduce


def get_operator(symbol: str) -> operator:
    return {
        "+": operator.add,
        "*": operator.mul,
    }[symbol]


def run(input: str) -> int:
    total = 0
    nums = defaultdict(list)
    *num_lines, symbol_line = input.splitlines()
    for line in num_lines:
        for i, c in enumerate(map(int, line.split())):
            nums[i].append(c)

    for col, op in enumerate(symbol_line.split()):
        total += reduce(get_operator(op), nums[col])

    return total
