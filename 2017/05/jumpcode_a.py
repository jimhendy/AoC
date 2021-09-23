class JumpCode:
    def __init__(self, code):
        self.code = list(map(int, code.split()))
        self.instruction_pointer = 0
        self.n_steps = 0

    def __call__(self):
        while True:
            try:
                jump = self.code[self.instruction_pointer]
                self.code[self.instruction_pointer] = jump + 1
                self.instruction_pointer += jump
                self.n_steps += 1
            except IndexError:
                return self.n_steps
