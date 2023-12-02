import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import ClassVar

MAX_CUBES = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


@dataclass
class Draw:
    draw_data: str

    _cube_reg: ClassVar[re.Pattern] = re.compile(r"((\d+) (\w+))")

    def cubes(self) -> Iterable[tuple[int, str]]:
        for draw in self._cube_reg.finditer(self.draw_data):
            yield int(draw.group(2)), draw.group(3)


@dataclass
class Game:
    line: str

    _game_reg: ClassVar[re.Pattern] = re.compile(r"^Game (\d+):")

    @property
    def id_(self) -> int:
        return int(self._game_reg.match(self.line).group(1))

    def draws(self) -> Iterable[Draw]:
        for draw_data in self.line.split(";"):
            yield Draw(draw_data)


def run(inputs: str) -> int:
    valid_id_sum = 0

    for line in inputs.splitlines():
        game = Game(line)

        if all(
            num <= MAX_CUBES[colour]
            for draw in game.draws()
            for num, colour in draw.cubes()
        ):
            valid_id_sum += game.id_

    return valid_id_sum
