import logging
import os
import re
import time
from collections import defaultdict

DEBUG = False

logger = logging.getLogger()
if DEBUG:
    logger.setLevel(logging.DEBUG)


class WrongOutputError(Exception):
    pass


class Assembunny:
    def __init__(self, instructions):
        self.instructions = self.extract_instructions(instructions)
        self.registers = defaultdict(lambda: 0)
        self.instruction_pointer = 0
        self.number_regex = re.compile("^-?\d+$")
        self.transmission_output = []

    def __call__(self):
        while len(self.transmission_output) < 50:
            logger.debug(self.registers)
            if len(self.transmission_output) > 1 and (
                any([i != 0 for i in self.transmission_output[::2]])
                or any([i != 1 for i in self.transmission_output[1::2]])
            ):
                raise WrongOutputError

            if DEBUG:
                time.sleep(0.5)
            try:
                self.check_for_cheat()
                func_name, *args = self.instructions[self.instruction_pointer]
                func = getattr(self, func_name)
                logger.debug(f"Running {func_name} with args {args}")
                func(*args)
            except IndexError:
                break

    def extract_instructions(self, instructions_str):
        return [i.split() for i in instructions_str.split(os.linesep)]

    def get_value(self, v):
        if self.number_regex.search(v):
            return int(v)
        else:
            return self.registers[v]

    def cpy(self, x, y):
        x_value = self.get_value(x)
        if not self.number_regex.search(y):
            self.registers[y] = x_value
            logger.debug(f"Copied {x_value} into {y}")
        else:
            logger.debug(f"Skipped cpy as y not value {y}")
        self.instruction_pointer += 1

    def inc(self, x, magnitude=1):
        if not self.number_regex.search(x):
            self.registers[x] += magnitude
            logger.debug(f"Incremented {x} to {self.registers[x]}")
        else:
            logger.debug(f"Skipped inc as x not value {x}")
        self.instruction_pointer += 1

    def dec(self, x, magnitude=1):
        if not self.number_regex.search(x):
            self.registers[x] -= magnitude
            logger.debug(f"Decresed {x} to {self.registers[x]}")
        else:
            logger.debug(f"Skipped dec as x not value {x}")
        self.instruction_pointer += 1

    def jnz(self, x, y):
        x_value = self.get_value(x)
        y_value = self.get_value(y)
        if x_value != 0:
            logger.debug(f"Jumped to instruction {y_value} away")
            self.instruction_pointer += int(y_value)
        else:
            self.instruction_pointer += 1

    def tgl(self, x):
        x_value = self.get_value(x)
        tgl_pointer = self.instruction_pointer + x_value
        if 0 < tgl_pointer < len(self.instructions):
            func_name, *args = self.instructions[tgl_pointer]

            if func_name == "tgl":
                new_func = "inc"
            elif len(args) == 1:
                if func_name == "inc":
                    new_func = "dec"
                else:
                    new_func = "inc"
            elif len(args) == 2:
                if func_name == "jnz":
                    new_func = "cpy"
                else:
                    new_func = "jnz"
            logger.debug(
                f"Toggling position {tgl_pointer}, {func_name} to {new_func} with args {args}"
            )
            self.instructions[tgl_pointer] = [new_func] + args

        self.instruction_pointer += 1

    def out(self, x):
        self.transmission_output.append(self.get_value(x))
        self.instruction_pointer += 1

    def check_for_cheat(self):
        letters = {}
        desired_funcs = [
            ("cpy", "b", "c"),
            ("inc", "a"),
            ("dec", "c"),
            ("jnz", "c", -2),
            ("dec", "d"),
            ("jnz", "d", -5),
        ]
        for i, df in enumerate(desired_funcs):
            func_name, *args = self.instructions[self.instruction_pointer + i]
            if not func_name == df[0]:
                return
            if not len(args) == len(df) - 1:
                return
            for df_a, a in zip(df[1:], args):
                if isinstance(df_a, int):
                    if not self.number_regex.search(a):
                        return
                    if df_a != int(a):
                        return
                else:
                    if df_a in letters.keys():
                        if a != letters[df_a]:
                            return
                    else:
                        letters[df_a] = a
        # Implement cheat
        a = letters["a"]
        b = letters["b"]
        d = letters["d"]
        c = letters["c"]

        a_value = self.get_value(a)
        b_value = self.get_value(b)
        d_value = self.get_value(d)

        logger.debug(
            f"Implementing cheat, {a} += {b} * {d} ({a_value} += {b_value} * {d_value})"
        )

        self.registers[a] += b_value * d_value
        self.registers[d] = 0
        self.registers[c] = 0

        self.instruction_pointer += len(desired_funcs)
