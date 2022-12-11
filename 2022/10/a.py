class Cpu:
    def __init__(self, instructions: str):
        self.instructions = iter(instructions.splitlines())
        self.cycles = 0
        self.x = 1
        self.x_inc = 0
        self.skip_cycles = 0
        self.total = 0

    def run(self):
        while self.cycles <= 220:
            self.cycles += 1

            if self.skip_cycles:
                self.skip_cycles -= 1
            else:
                self.parse_instruction()

            self.check_signal_strength()

            if not self.skip_cycles:
                self.apply_instruction()

    def parse_instruction(self):
        op_name, *op_args = next(self.instructions).split()
        getattr(self, op_name)(*op_args)

    def noop(self):
        assert not self.skip_cycles

    def addx(self, arg: str):
        self.x_inc = int(arg)
        self.skip_cycles = 1

    def apply_instruction(self):
        self.x += self.x_inc
        self.x_inc = 0

    def check_signal_strength(self):
        if not (self.cycles - 20) % 40:
            self.total += self.cycles * self.x


def run(inputs):

    cpu = Cpu(instructions=inputs)
    cpu.run()

    return cpu.total
