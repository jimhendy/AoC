import functools
import re


def increment_pointer(func):
    @functools.wraps(func)
    def wrapped(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.instruction_pointer += 1
        return result

    return wrapped


class BootCode:
    def __init__(self, instructions):
        self.instructions = self.extract_instructions(instructions)
        self.instruction_pointer = 0
        self.accumulator = 0
        self.seen_instructions = set()

    def extract_instructions(self, instructions):
        ins = []
        for i in instructions:
            match = re.findall(r"(\w+) ([\+\-\d]+)", i)[0]
            ins.append((getattr(self, match[0]), int(match[1])))
        return ins

    def run(self):
        while self.instruction_pointer not in self.seen_instructions:
            if self.instruction_pointer == len(self.instructions):
                # Reached the natural end of the code
                return
            self.seen_instructions.add(self.instruction_pointer)
            func, arg = self.instructions[self.instruction_pointer]
            func(arg)
        return self.accumulator

    @increment_pointer
    def acc(self, arg):
        self.accumulator += arg

    def jmp(self, arg):
        self.instruction_pointer += arg

    @increment_pointer
    def nop(self, arg):
        pass
