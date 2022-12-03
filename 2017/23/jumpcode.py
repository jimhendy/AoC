import re
import time
from collections import defaultdict


class JumpCode:
    def __init__(self, instructions, bail_func=None, debug_mode=False):
        self.instructions = instructions
        self.instruction_pointer = 0
        self.registers = defaultdict(int)
        self.debug_mode = debug_mode
        if not self.debug_mode:
            self.registers["a"] = 1
        self.instruction_nums = defaultdict(int)

    def run(self):
        i = 0
        while True:
            i += 1
            try:
                ins = self.instructions[self.instruction_pointer]
            except IndexError:
                break

            print(self.instruction_pointer)

            if i > 10_000:
                break
            func_name, *args = ins.split()
            func = getattr(self, func_name)
            self.instruction_nums[func_name] += 1
            func(*args)

            print(ins)
            print(self.registers)
            print("*" * 30)
            pass
        pass

    def _get_value(self, value):
        if isinstance(value, (int, float)) or (
            isinstance(value, str) and re.match(r"^(\-?\d+)$", value)
        ):
            return int(value)
        elif isinstance(value, str):
            return self._get_value(self.registers[value])
        else:
            raise NotImplementedError(
                f'Expected value to be a string or int, found "{value}", type: "{type(value)}"'
            )

    def set(self, x, y):
        self.registers[x] = self._get_value(y)
        self.instruction_pointer += 1

    def sub(self, x, y):
        self.registers[x] -= self._get_value(y)
        self.instruction_pointer += 1

    def mul(self, x, y):
        self.registers[x] *= self._get_value(y)
        self.instruction_pointer += 1

    def jnz(self, x, y):
        if self._get_value(x) != 0:
            self.instruction_pointer += self._get_value(y)
        else:
            self.instruction_pointer += 1
