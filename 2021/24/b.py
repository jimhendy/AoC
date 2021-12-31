from collections import deque
import os
import re
import numpy as np
import pandas as pd
from tools.binary_search import binary_search
from collections import deque
from typing import List


class ArithmeticLogicUnit:
    def __init__(self, instructions: List[str]):
        self.instructions = instructions
        self.inputs = None
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

    def get(self, name: str):
        if name in {"w", "x", "y", "z"}:
            return getattr(self, name)
        else:
            return int(name)

    def run(self, inputs: deque):
        self.inputs = inputs
        for ins in self.instructions:
            ins_code, *args = ins.split()
            getattr(self, ins_code)(*args)

    def inp(self, a):
        setattr(self, a, self.inputs.popleft())

    def add(self, a, b):
        setattr(self, a, getattr(self, a) + self.get(b))

    def mul(self, a, b):
        setattr(self, a, getattr(self, a) * self.get(b))

    def div(self, a, b):
        setattr(self, a, getattr(self, a) // self.get(b))

    def mod(self, a, b):
        setattr(self, a, getattr(self, a) % self.get(b))

    def eql(self, a, b):
        setattr(self, a, int(getattr(self, a) == self.get(b)))


def get_constraints(instructions):
    constraints = []
    stack = deque()
    line = 0

    for i in range(14):
        line += 4
        op = instructions[line].rstrip()

        assert op.startswith("div z "), f'Invalid input! "{op}", "{line}"'

        if op == "div z 1":  # first kind of chunk
            line += 11
            op = instructions[line]
            line += 3
            assert op.startswith("add y "), "Invalid input!"

            a = int(op.split()[-1])  # first constant to add
            stack.append((i, a))
        else:  # second kind of chunk
            line += 1
            op = instructions[line]
            line += 13
            assert op.startswith("add x "), "Invalid input!"

            b = int(op.split()[-1])  # second constant to add
            j, a = stack.pop()
            constraints.append((i, j, a + b))  # digits[j] - digits[i] must equal a + b

    return constraints


def find_min(constraints):
    digits = [0] * 14

    for i, j, diff in constraints:
        if diff > 0:
            digits[i], digits[j] = 1 + diff, 1
        else:
            digits[i], digits[j] = 1, 1 - diff

    # Compute the actual number from its digits.
    num = 0
    for d in digits:
        num = num * 10 + d

    return num


def run(inputs):
    lines = inputs.split(os.linesep)
    alu = ArithmeticLogicUnit(lines)

    constraints = get_constraints(lines)
    min_num = find_min(constraints)
    deq = deque([int(i) for i in str(min_num)])

    alu.run(deq)
    assert alu.z == 0

    return min_num
