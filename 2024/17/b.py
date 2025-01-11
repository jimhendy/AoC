from dataclasses import dataclass, field
from typing import ClassVar, Callable
from functools import wraps
import re
from computer import find_a


def run(inputs: str) -> int:
    registers, program = inputs.strip().split("\n\n")
    regregex = re.compile(r"Register (\w): (\d+)")
    registers = {m.group(1): int(m.group(2)) for m in regregex.finditer(registers)}
    program = list(map(int, program.split(":")[1].split(",")))

    result = find_a(registers, program)

    return result
