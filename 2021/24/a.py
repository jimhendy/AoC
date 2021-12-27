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
        if name in {'w','x','y','z'}:
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


def run(inputs):
    alu = ArithmeticLogicUnit(inputs.split(os.linesep))
    
    return alu.z
