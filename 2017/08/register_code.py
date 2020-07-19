import re
from functools import partial
from collections import defaultdict


class RegisterCode:

    def __init__(self, code_text):
        self.registers = defaultdict(int)
        self.code = self.extract_code(code_text)
        self.history = []

    def __call__(self):
        for c in self.code:
            if c['test']():
                c['alter']()
            self.history.append(self.registers.copy())
        pass

    def extract_code(self, code_text):
        return [
            {
                'alter': partial(getattr(self, m[1]), register=m[0], value=m[2]),
                'test': partial(self.test, *m[3:])
            }
            for m in
            re.findall(
                r'(\w+) (inc|dec) ([-\d+]+) if (\w+) (.+) ([-\d+]+)',
                code_text
            )
        ]

    def inc(self, register, value):
        self.registers[register] += int(value)

    def dec(self, register, value):
        self.inc(register, -1 * int(value))

    def test(self, register, comparison_str, comparison_value):
        return eval(f'int({self.registers[register]}) {comparison_str} int({comparison_value})')