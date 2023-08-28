import re
from collections import defaultdict


class JumpCode:
    def __init__(self, instructions, bail_func=None) -> None:
        self.instructions = instructions
        self.instruction_pointer = 0
        self.registers = defaultdict(int)
        self.played_sounds = []
        self.recovered_sounds = []
        self.bail_func = bail_func

    def run(self):
        while True:
            try:
                ins = self.instructions[self.instruction_pointer]
            except IndexError:
                return None

            func_name, *args = ins.split()
            func = getattr(self, func_name)

            func(*args)

            if self.bail_func is not None:
                ret = self.bail_func(self)
                if ret is not None:
                    return ret

            pass
        pass
        return None

    def _get_value(self, value):
        if isinstance(value, int | float) or (
            isinstance(value, str) and re.match(r"^(\-?\d+)$", value)
        ):
            return int(value)
        elif isinstance(value, str):
            return self._get_value(self.registers[value])
        else:
            msg = f'Expected value to be a string or int, found "{value}", type: "{type(value)}"'
            raise NotImplementedError(
                msg,
            )

    def snd(self, x):
        freq = self._get_value(x)
        self.played_sounds.append(freq)
        self.instruction_pointer += 1

    def set(self, x, y):
        self.registers[x] = self._get_value(y)
        self.instruction_pointer += 1

    def add(self, x, y):
        self.registers[x] += self._get_value(y)
        self.instruction_pointer += 1

    def mul(self, x, y):
        self.registers[x] *= self._get_value(y)
        self.instruction_pointer += 1

    def mod(self, x, y):
        self.registers[x] %= self._get_value(y)
        self.instruction_pointer += 1

    def rcv(self, x):
        self.instruction_pointer += 1
        if self._get_value(x):
            sound = self.played_sounds[-1]
            self.recovered_sounds.append(sound)

    def jgz(self, x, y):
        if self._get_value(x) > 0:
            self.instruction_pointer += self._get_value(y)
        else:
            self.instruction_pointer += 1
