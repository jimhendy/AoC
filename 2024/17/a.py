from dataclasses import dataclass, field
from typing import ClassVar, Callable
from functools import wraps
import re


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
    registers: dict[str, int]

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


def run(inputs: str) -> int:
    registers, program = inputs.strip().split("\n\n")
    regregex = re.compile(r"Register (\w): (\d+)")
    registers = {m.group(1): int(m.group(2)) for m in regregex.finditer(registers)}
    program = list(map(int, program.split(":")[1].split(",")))
    computer = Computer(program, registers)
    computer.run()
    print(",".join(map(str, computer.outputs)))
    return 0
