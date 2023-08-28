class CpuCrt:
    def __init__(self, instructions: str) -> None:
        self.instructions = iter(instructions.splitlines())
        self.cycles = 0
        self.x = 1
        self.x_inc = 0
        self.skip_cycles = 0
        self.output = ""

    def run(self):
        try:
            while True:
                self.cycles += 1

                if self.skip_cycles:
                    self.skip_cycles -= 1
                else:
                    self.parse_instruction()

                self.add_pixel()

                if not self.skip_cycles:
                    self.apply_instruction()
        except StopIteration:
            self.output = "\n".join(
                [
                    self.output[start : start + 40]
                    for start in range(0, len(self.output), 40)
                ],
            )

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

    def add_pixel(self):
        self.output += "#."[abs(self.x - (self.cycles - 1) % 40) > 1]


def run(inputs):
    cpu = CpuCrt(instructions=inputs)
    cpu.run()

    print(cpu.output)
