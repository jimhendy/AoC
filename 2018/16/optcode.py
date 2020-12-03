import functools
import re


def write_to_c(func):
    @functools.wraps(func)
    def wrapped(self, A, B, C):
        self.registers[C] = func(self, A, B, C)

    return wrapped


def get_reg_a(func):
    @functools.wraps(func)
    def wrapped(self, A, B, C):
        return func(self, self.registers[A], B, C)

    return wrapped


def get_reg_b(func):
    @functools.wraps(func)
    def wrapped(self, A, B, C):
        return func(self, A, self.registers[B], C)

    return wrapped


class OptCode:
    def __init__(self, instructions):
        self.instructions = instructions
        self.registers = [0] * 4
        self.instruction_reg = re.compile(r"([\-\d]+) ([\-\d]+) ([\-\d]+) ([\-\d]+)")
        self.function_mapping = {
            0: "bani",
            1: "gtri",
            2: "seti",
            3: "eqir",
            4: "eqrr",
            5: "borr",
            6: "bori",
            7: "banr",
            8: "muli",
            9: "eqri",
            10: "mulr",
            11: "gtrr",
            12: "setr",
            13: "addr",
            14: "gtir",
            15: "addi"
        }

    def run(self):
        for i in self.instructions:
            matches = self.instruction_reg.findall(i)[0]
            func = getattr(self, self.function_mapping[int(matches[0])])
            func(*list(map(int, matches[1:])))

    ## ADD

    @write_to_c
    @get_reg_a
    @get_reg_b
    def addr(self, A, B, C):
        return A + B

    @write_to_c
    @get_reg_a
    def addi(self, A, B, C):
        return A + B

    # MUL

    @write_to_c
    @get_reg_a
    @get_reg_b
    def mulr(self, A, B, C):
        return A * B

    @write_to_c
    @get_reg_a
    def muli(self, A, B, C):
        return A * B

    ## BITWISE AND

    @write_to_c
    @get_reg_a
    @get_reg_b
    def banr(self, A, B, C):
        return A & B

    @write_to_c
    @get_reg_a
    def bani(self, A, B, C):
        return A & B

    ## BITWISE OR

    @write_to_c
    @get_reg_a
    @get_reg_b
    def borr(self, A, B, C):
        return A | B

    @write_to_c
    @get_reg_a
    def bori(self, A, B, C):
        return A | B

    ## Assignment

    @write_to_c
    @get_reg_a
    def setr(self, A, B, C):
        return A

    @write_to_c
    def seti(self, A, B, C):
        return A

    ## Greater than testing

    @write_to_c
    @get_reg_b
    def gtir(self, A, B, C):
        return int(A > B)

    @write_to_c
    @get_reg_a
    def gtri(self, A, B, C):
        return int(A > B)

    @write_to_c
    @get_reg_a
    @get_reg_b
    def gtrr(self, A, B, C):
        return int(A > B)

    ## Equality Testing

    @write_to_c
    @get_reg_b
    def eqir(self, A, B, C):
        return int(A == B)

    @write_to_c
    @get_reg_a
    def eqri(self, A, B, C):
        return int(A == B)

    @write_to_c
    @get_reg_a
    @get_reg_b
    def eqrr(self, A, B, C):
        return int(A == B)
