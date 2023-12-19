import re
from collections import deque
from dataclasses import dataclass, field

DAMAGED_REGEX = re.compile("#+")
DAMAGED_OR_UNKNOWN = r"(?:#|\?)"
EMPTY_OR_UNKNOWN = r"(?:\?|\.)"


@dataclass(slots=True)
class SpringRow:
    initial_state: str
    damaged_springs: list[int]
    valid_regex: re.Pattern = field(init=False)

    def __post_init__(self):
        regex = f"^{EMPTY_OR_UNKNOWN}*"
        for num_damaged in self.damaged_springs[:-1]:
            regex += f"{DAMAGED_OR_UNKNOWN}{{{num_damaged}}}{EMPTY_OR_UNKNOWN}+"
        regex += (
            f"{DAMAGED_OR_UNKNOWN}{{{self.damaged_springs[-1]}}}{EMPTY_OR_UNKNOWN}*$"
        )
        self.valid_regex = re.compile(regex)

    def is_valid_solution(self, state: str) -> bool:
        damaged_groups = DAMAGED_REGEX.findall(state)
        return [len(group) for group in damaged_groups] == self.damaged_springs

    def is_valid_state(self, state: str) -> bool:
        return self.valid_regex.search(state)

    def solutions(self) -> list[str]:
        possibles = deque([self.initial_state])
        solutions = []

        while possibles:
            state = possibles.popleft()

            if "?" not in state:
                # No more damaged springs
                if self.is_valid_solution(state):
                    solutions.append(state)
            else:
                # We have more damaged springs
                if not self.is_valid_state(state):
                    continue
                # Replace the first unknown (?) with a "." and a "#" and try again
                for i in range(len(state)):
                    if state[i] == "?":
                        new_state = state[:i] + "." + state[i + 1 :]
                        possibles.append(new_state)
                        new_state = state[:i] + "#" + state[i + 1 :]
                        possibles.append(new_state)
                        break

        return solutions


def run(inputs: str) -> int:
    total = 0

    lines = inputs.splitlines()
    num_lines = len(lines)

    for i, line in enumerate(lines):
        print(f"{line} {i}/{num_lines}")
        state, damaged = line.split()

        state = "?".join([state for _ in range(5)])

        damaged_springs = list(map(int, damaged.split(",")))
        damaged_springs = 5 * damaged_springs

        spring_row = SpringRow(state, damaged_springs)
        total += len(spring_row.solutions())

    return total
