import re

INS_REG = re.compile("^(\w{3}) (.+)$")


class Computer:
    def __init__(self, code):
        self.a = 0
        self.b = 0
        self.code = code
        self.instruction_pointer = 0

    def extract_instruction(self, ins):
        func, args = INS_REG.findall(ins)[0]
        return getattr(self, func), args.split(",")

    def run(self):
        while True:
            if self.instruction_pointer < 0 or self.instruction_pointer >= len(
                self.code
            ):
                break
            next_instruction = self.code[self.instruction_pointer]
            func, args = self.extract_instruction(next_instruction)
            func(*args)

    def hlf(self, register):
        setattr(self, register, getattr(self, register) / 2)
        self.instruction_pointer += 1

    def tpl(self, register):
        setattr(self, register, getattr(self, register) * 3)
        self.instruction_pointer += 1

    def inc(self, register):
        setattr(self, register, getattr(self, register) + 1)
        self.instruction_pointer += 1

    def jmp(self, offset):
        self.instruction_pointer += int(offset)

    def jio(self, register, offset):
        if getattr(self, register) == 1:
            self.jmp(offset)
        else:
            self.instruction_pointer += 1

    def jie(self, register, offset):
        if getattr(self, register) % 2 == 0:
            self.jmp(offset)
        else:
            self.instruction_pointer += 1
