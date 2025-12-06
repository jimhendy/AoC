import operator
from dataclasses import dataclass
from functools import reduce

import numpy as np


def get_operator(symbol: str) -> operator:
    return {
        "+": operator.add,
        "*": operator.mul,
    }[symbol]


def row_to_int(row):
    num_str = ""
    for c in row:
        if c == " ":
            continue
        num_str += c
    if num_str == "":
        return 0
    return int(num_str)


@dataclass
class OperatorGroup:
    operator: str
    nums_count: int


def run(input: str) -> int:
    *num_lines, symbol_line = input.splitlines()

    operators = []
    n_chars = 0
    for c in symbol_line[::-1]:
        n_chars += 1
        if c == " ":
            continue
        operators.append(OperatorGroup(get_operator(c), n_chars))
        n_chars = 0

    nums = np.array([list(i) for i in num_lines]).T[::-1]
    nums = [row_to_int(row) for row in nums]

    total = 0
    i = 0
    for op_group in operators:
        nums_slice = [i for i in nums[i : i + op_group.nums_count] if i]
        print(nums_slice, op_group)
        total += reduce(op_group.operator, nums_slice)
        i += op_group.nums_count
    return total
