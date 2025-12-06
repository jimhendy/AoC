import logging
import os
from collections import defaultdict
from functools import partial

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class Assembunny:
    def __init__(self, instructions) -> None:
        self.instructions = self.extract_instructions(instructions)
        self.registers = defaultdict(lambda: 0)
        self.instruction_pointer = 0

    def __call__(self):
        while True:
            try:
                ins = self.instructions[self.instruction_pointer]
                ins()
            except IndexError:
                break

    def extract_instructions(self, instructions_str):
        instructions = []
        for i in instructions_str.split(os.linesep):
            func_name, *args = i.split()
            func = getattr(self, func_name)
            instructions.append(partial(func, *args))
        return instructions

    def get_value(self, v):
        if v.isdigit():
            return int(v)
        return self.registers[v]

    def cpy(self, x, y):
        x_value = self.get_value(x)
        self.registers[y] = x_value
        logger.debug(f"Copied {x_value} into {y}")
        self.instruction_pointer += 1

    def inc(self, x, magnitude=1):
        self.registers[x] += magnitude
        logger.debug(f"Incremented {x} to {self.registers[x]}")
        self.instruction_pointer += 1

    def dec(self, x, magnitude=1):
        self.registers[x] -= magnitude
        logger.debug(f"Decresed {x} to {self.registers[x]}")
        self.instruction_pointer += 1

    def jnz(self, x, y):
        x_value = self.get_value(x)
        if x_value != 0:
            logger.debug(f"Jumped to instruction {y}")
            self.instruction_pointer += int(y)
        else:
            self.instruction_pointer += 1
