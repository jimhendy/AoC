import re
from collections.abc import Iterable

from tools.a_star import State as _State
from tools.a_star import a_star

REGEX = re.compile(
    r"\[(?P<aim>[.#]+)\](?P<buttons>(?: \([0-9,]+\))+?) \{(?P<joltage>[0-9, ]+)\}",
)


class State(_State):
    def __init__(
        self,
        aim: set[int],
        buttons: list[set[int]],
        lights: set[int],
        history: list[int],
    ) -> None:
        self.aim = aim
        self.buttons = buttons
        self.lights = lights
        self.history = history

    def is_complete(self) -> bool:
        return self.lights == self.aim

    def all_possible_next_states(self) -> Iterable["State"]:
        for i, b in enumerate(self.buttons):
            new_lights = self.lights.symmetric_difference(b)
            new_history = self.history + [i]
            yield State(self.aim, self.buttons, new_lights, new_history)

    def is_valid(self) -> bool:
        return True

    def __lt__(self, other: _State) -> bool:
        return len(self.history) < len(other.history)

    def __repr__(self) -> str:
        return str(self.lights)


def run(input: str) -> int:
    total = 0
    for line in input.splitlines():
        match = REGEX.match(line)

        if not match:
            msg = f"Line does not match expected format: {line}"
            raise ValueError(msg)

        aim_str = match.group("aim")
        buttons_str = match.group("buttons").strip().split(" ")

        aim = {i for i, c in enumerate(aim_str) if c == "#"}
        buttons = [set(map(int, b[1:-1].split(","))) for b in buttons_str]

        initial_lights = set()
        initial_state = State(aim, buttons, initial_lights, [])

        solution = a_star(initial_state)
        if solution is not None:
            total += len(solution.history)

    return total
