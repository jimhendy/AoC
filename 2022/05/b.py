import pathlib
import re
from queue import LifoQueue
from typing import List, Tuple

INSTRUCTION_REG = re.compile(r"^move (\d+) from (\d+) to (\d+)$")


class Stack:
    def __init__(self, crates: List[List[str]]) -> None:
        self.crates = {}
        for stack_num in range(len(crates[0])):
            self.crates[stack_num + 1] = LifoQueue()
            for row in reversed(crates):
                if row[stack_num] != " ":
                    self.crates[stack_num + 1].put(row[stack_num])


def _parse_instruction(line: str) -> List[int]:
    return list(map(int, INSTRUCTION_REG.findall(line)[0]))


def _parse_crates(line: str, num_stacks: int) -> List[str]:
    reg = re.compile(".".join([".(.)."] * num_stacks))
    return reg.findall(line)[0]


def parse_inputs(inputs: str) -> Tuple[List[List[str]], List[List[int]], int]:
    crates = []
    unparsed_crates = []
    instructions = []
    num_stacks = None

    crates_complete = False

    for line in inputs.splitlines():
        if not line.strip():
            continue
        if crates_complete:
            instructions.append(_parse_instruction(line))
        else:
            if all([line_character.isnumeric() for line_character in line.split()]):
                num_stacks = int(line.split()[-1])
                crates = [_parse_crates(c, num_stacks) for c in unparsed_crates]
                crates_complete = True
            else:
                unparsed_crates.append(line)

    return crates, instructions, num_stacks


def run(inputs: str) -> str:
    initial_crates, instructions, num_stacks = parse_inputs(inputs)
    stack = Stack(initial_crates)

    temp_queue = LifoQueue()

    for moves, from_, to in instructions:
        [temp_queue.put(stack.crates[from_].get()) for _ in range(moves)]
        [stack.crates[to].put(temp_queue.get()) for _ in range(moves)]

    return "".join(stack.crates[i].get() for i in range(1, num_stacks + 1))
