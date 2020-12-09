import functools
import re
from collections import defaultdict

def write_to_c(func):
    @functools.wraps(func)
    def wrapped(self, A, B, C):
        self.registers[self.ip_reg] = self.instruction_pointer
        self.registers[C] = func(self, A, B, C)
        self.instruction_pointer = self.registers[self.ip_reg] + 1


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
    def __init__(self, instruction_pointet_register, instructions):
        self.ip_reg = instruction_pointet_register
        self.instruction_pointer = 0
        self.instructions = instructions
        self.registers = [0] * 6
        self.instruction_reg = re.compile(r"(\w+) ([\-\d]+) ([\-\d]+) ([\-\d]+)")
        self.instruction_count = defaultdict(int) # instruction_id : count
        self.instruction_count_order = defaultdict(list) # count : list([instructions_pointers])

    def run(self):
        while True:
            '''
            print(self.registers)

            if self.registers[self.ip_reg] == 3:
                if not self.registers[4] % self.registers[2]:
                    self.registers[3] = self.registers[1]
                    self.registers[5] = 1
                    self.registers[self.ip_reg] = 7
                else:
                    self.registers[3] = self.registers[1] + 1
                    self.registers[5] = 1
                    self.registers[self.ip_reg] = 12
                self.instruction_pointer = self.registers[self.ip_reg] + 1
                continue

            try:
                i = self.instructions[self.instruction_pointer]
            except IndexError:
                return
            
            self.instruction_count[self.instruction_pointer] += 1
            self.instruction_count_order[self.instruction_count[self.instruction_pointer]].append(i)
            if len(self.instruction_count_order[self.instruction_count[self.instruction_pointer]]) == 1:
                print('='*30)
            print(self.instruction_count_order[self.instruction_count[self.instruction_pointer]])
            '''
            matches = self.instruction_reg.findall(i)[0]
            func = getattr(self, matches[0])
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
