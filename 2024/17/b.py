import re
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import ClassVar

from loguru import logger


class InvalidAValueError(Exception):
    """Custom exception for invalid value of register A."""


def combo(func: callable) -> callable:
    @wraps(func)
    def wrapper(self, operand: int) -> int:
        operand_value = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: self.registers["A"],
            5: self.registers["B"],
            6: self.registers["C"],
        }[operand]
        return func(self, operand_value)

    return wrapper


def output_to_register(register: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, operand: int) -> int:
            result = func(self, operand)
            self.registers[register] = result
            return result

        return wrapper

    return decorator


def increment_instruction_pointer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, operand: int) -> int:
        result = func(self, operand)
        self.instruction_pointer += 2
        return result

    return wrapper


@dataclass
class Computer:
    program: list[int]
    registers: dict[str, int] = field(default_factory=lambda: {"A": 0, "B": 0, "C": 0})

    opcode_mapping: ClassVar[dict[int, str]] = {
        0: "adv",
        1: "bxl",
        2: "bst",
        3: "jnz",
        4: "bxc",
        5: "out",
        6: "bdv",
        7: "cdv",
    }

    instruction_pointer: int = field(init=False, default=0)
    outputs: list[int] = field(default_factory=list, init=False)

    def run(self) -> None:
        while self.instruction_pointer < len(self.program):
            opcode, operand = (
                self.program[self.instruction_pointer],
                self.program[self.instruction_pointer + 1],
            )
            opcode_name = self.opcode_mapping[opcode]
            getattr(self, f"_{opcode_name}")(operand)

    def reset(self, register_a: int) -> None:
        self.registers["A"] = register_a
        self.registers["B"] = 0
        self.registers["C"] = 0
        self.instruction_pointer = 0
        self.outputs.clear()
        self.expected_output = ",".join(map(str, self.program))

    def _compare(self, num_chars_matching: int | None = None) -> bool:
        if num_chars_matching is None:
            num_chars_matching = len(self.program)
        program = self.program[-num_chars_matching:]
        outputs = self.outputs[-num_chars_matching:]

        for p, o in zip(program, outputs, strict=False):
            if p != o:
                return False
        return True

    def valid_outputs(self) -> bool:
        if not self.outputs:
            return True
        return self._compare()

    def matching_output(self, num_chars_matching: int | None = None) -> bool:
        if not self.outputs:
            return False
        return self._compare(num_chars_matching)

    def _adv_calc(self, operand: int) -> int:
        return self.registers["A"] // 2**operand

    @combo
    @output_to_register("A")
    @increment_instruction_pointer
    def _adv(self, operand: int) -> int:
        return self._adv_calc(operand)

    @output_to_register("B")
    @increment_instruction_pointer
    def _bxl(self, operand: int) -> int:
        return self.registers["B"] ^ operand

    @combo
    @output_to_register("B")
    @increment_instruction_pointer
    def _bst(self, operand: int) -> int:
        return operand & 7

    def _jnz(self, operand: int) -> None:
        if self.registers["A"] == 0:
            self.instruction_pointer += 2
            return
        self.instruction_pointer = operand

    @increment_instruction_pointer
    @output_to_register("B")
    def _bxc(self, operand: int) -> None:
        return self.registers["B"] ^ self.registers["C"]

    @combo
    @increment_instruction_pointer
    def _out(self, operand: int) -> None:
        result = operand % 8
        self.outputs.append(result)

    @combo
    @output_to_register("B")
    @increment_instruction_pointer
    def _bdv(self, operand: int) -> int:
        return self._adv_calc(operand)

    @combo
    @output_to_register("C")
    @increment_instruction_pointer
    def _cdv(self, operand: int) -> int:
        return self._adv_calc(operand)


def binary_to_decimal(binary_list: list[int]) -> int:
    """Convert a list of binary digits to a decimal number."""
    return sum(bit * (2**idx) for idx, bit in enumerate(reversed(binary_list)))


def decimal_to_binary(decimal: int) -> list[int]:
    """Convert a decimal number to a list of binary digits."""
    if decimal == 0:
        return [0]
    binary = []
    while decimal > 0:
        binary.append(decimal % 2)
        decimal //= 2
    return list(reversed(binary))


def all_combinations(
    computer: Computer,
    n_matching: int,
    previous_combinations: list[list[int]],
) -> list[list[int]]:
    combinations = []
    step = 3
    for previous in previous_combinations:
        start = binary_to_decimal(previous + [0] * step)
        end = binary_to_decimal(previous + [1] * step) + 1

        for a in range(start, end):
            computer.reset(a)
            try:
                computer.run()
                if computer.matching_output(n_matching):
                    known_value = decimal_to_binary(a)
                    combinations.append(known_value)
            except InvalidAValueError:
                continue

    return combinations


def run(inputs: str) -> int:
    registers, program = inputs.strip().split("\n\n")
    regregex = re.compile(r"Register (\w): (\d+)")
    registers = {m.group(1): int(m.group(2)) for m in regregex.finditer(registers)}
    program = list(map(int, program.split(":")[1].split(",")))

    computer = Computer(program)
    possibles = [[]]
    n_matching = 1

    for n_matching in range(1, len(program) + 1):
        new_combinations = all_combinations(computer, n_matching, possibles)
        if not new_combinations:
            logger.warning("No new combinations found, stopping search.")
            break
        possibles = new_combinations

    decimals = [binary_to_decimal(combination) for combination in possibles]
    sorted_decimals = sorted(decimals)

    return sorted_decimals[0]
