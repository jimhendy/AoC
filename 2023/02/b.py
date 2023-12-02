import re
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from functools import reduce
from operator import mul
from typing import ClassVar


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

    def power(self) -> int:
        min_cubes = defaultdict(int)

        for draw in self.draws():
            for num, colour in draw.cubes():
                min_cubes[colour] = max(min_cubes[colour], num)

        return reduce(mul, min_cubes.values(), 1)


def run(inputs: str) -> int:
    return sum(Game(line).power() for line in inputs.splitlines())
