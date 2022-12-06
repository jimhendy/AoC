import pathlib
import re
from typing import List, Tuple
from collections import defaultdict, deque

INSTRUCTION_REG = re.compile(r"^move (\d+) from (\d+) to (\d+)$")


def run(inputs: str) -> str:
    inputs = inputs.splitlines()

    initial_crates = []
    instructions_starting_line = None
    num_stacks = None
    crates_complete = False

    for line_num, line in enumerate(inputs):
        if not line.strip():
            continue
        if crates_complete:
            instructions_starting_line = line_num
            break
        else:
            if all(line_character.isnumeric() for line_character in line.split()):
                num_stacks = int(line.split()[-1])
                stacks_reg = re.compile(" ".join([".(.)."] * num_stacks))
                initial_crates = [stacks_reg.findall(c)[0] for c in initial_crates]
                crates_complete = True
            else:
                initial_crates.append(line)

    crates = defaultdict(deque)
    for stack_num in range(num_stacks):
        for row in reversed(initial_crates):
            if row[stack_num] != " ":
                crates[stack_num + 1].append(row[stack_num])

    for instruction_line in inputs[instructions_starting_line:]:
        moves, from_, to = map(int, INSTRUCTION_REG.findall(instruction_line)[0])
        [crates[to].append(crates[from_].pop()) for _ in range(moves)]

    return "".join(crates[i].pop() for i in range(1, num_stacks + 1) if len(crates[i]))
