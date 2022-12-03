import re
from collections import defaultdict
from functools import lru_cache

import tqdm


class Turing:
    def __init__(self, instructions):
        self.tape = defaultdict(int)
        self.cursor = 0
        self.instructions = instructions
        self.state = self.extract_inital_state()
        self.steps = self.extract_steps()
        print(
            f"Turning machine created with initial state {self.state} and {self.steps:,} steps."
        )

    def extract_inital_state(self):
        reg = re.compile(r"Begin in state ([A-Z])\.")
        return reg.findall(self.instructions)[0]

    def extract_steps(self):
        reg = re.compile(r"Perform a diagnostic checksum after (\d+) steps\.")
        return int(reg.findall(self.instructions)[0])

    def __call__(self):
        for _ in tqdm.tqdm(range(self.steps)):
            value = self.tape[self.cursor]
            data = self.extract_instruction_data(self.state, value)
            self.tape[self.cursor] = data["WriteValue"]
            if data["MoveLeft"]:
                self.cursor -= 1
            else:
                self.cursor += 1
            self.state = data["NewState"]

    @lru_cache(1024)
    def extract_instruction_data(self, state, value):
        reg = Turing.generate_regex(state, value)
        try:
            match = re.findall(reg, self.instructions)[0]
        except:
            # import pdb

            # pdb.set_trace()
            pass
        return {
            "WriteValue": int(match[0]),
            "MoveLeft": match[1] == "left",
            "NewState": match[2],
        }

    @staticmethod
    def generate_regex(current_state, current_value):
        return r"[\s\S]*?".join(
            [
                f"In state {current_state}:",
                f"If the current value is {current_value}:",
                r"Write the value (\d)\.",
                r"Move one slot to the (\w+)\.",
                r"Continue with state ([A-Z])\.",
            ]
        )
