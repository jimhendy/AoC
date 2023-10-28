from dataclasses import dataclass
from enum import Enum
from typing import Union

import numpy as np


class Direction(Enum):
    LEFT = 0
    RIGHT = 1


@dataclass
class Explosion:
    direction: Direction
    value: int


class Pair:
    def __init__(self, left: Union["Pair", int], right: Union["Pair", int]) -> None:
        self.left = left
        self.right = right
        self.left_int = isinstance(self.left, int)
        self.right_int = isinstance(self.right, int)

    def copy(self):
        return Pair(
            left=self.left if self.left_int else self.left.copy(),
            right=self.right if self.right_int else self.right.copy(),
        )

    def magnitude(self):
        l = self.left if self.left_int else self.left.magnitude()
        r = self.right if self.right_int else self.right.magnitude()
        return 3 * l + 2 * r

    def reduce(self):
        while True:
            if self.explode_nested_pairs():
                continue
            if self.split_large_values():
                continue
            break

    def _add_number_from_explode(self, number: int, leftmost: bool):
        """
        An explosion has occured and we need to add a value to the leftmost
        or rightmost number in this pair. Travserse child pairs until we find a
        number to add to.
        """
        if leftmost:
            if self.left_int:
                self.left += number
            else:
                self.left._add_number_from_explode(number, leftmost)
        else:
            if self.right_int:
                self.right += number
            else:
                self.right._add_number_from_explode(number, leftmost)

    def explode_nested_pairs(self, level=0) -> bool | list[Explosion]:
        """
        Check all sub-pairs for any nested at level 4 and explode if found.

        If no explosion occurs, return ``False``.
        If an explosion occurs but are handled at this level, return ``True``.
        If unhandled ``Explosion``s occur, return a ``list`` of them.
        """
        if level > 4:
            msg = f"Level should not get this high, {level}, {self}"
            raise RuntimeError(msg)
        elif level == 4:
            assert self.left_int and self.right_int, (
                f'Expected two ints at this level but found left="{self.left}", '
                f'right="{self.right}"'
            )
            return [
                Explosion(Direction.LEFT, self.left),
                Explosion(Direction.RIGHT, self.right),
            ]
        # Would like to wrap the below into a method to avoid repeated code but unsure
        # how to then assign with e.g. self.right += e.value as passing self.right
        # would not work due to scoping
        if not self.left_int:
            ex = self.left.explode_nested_pairs(level=level + 1)
            if ex is False:
                pass
            elif ex is True:
                return True
            else:
                if level == 3:
                    # Explosion occured at this node, zero and adjust int flag
                    self.left = 0
                    self.left_int = True
                return_exs = []
                for e in ex:
                    if e.direction is Direction.RIGHT:
                        if self.right_int:
                            self.right += e.value
                        else:
                            self.right._add_number_from_explode(e.value, leftmost=True)
                    else:
                        return_exs.append(e)

                return return_exs if len(return_exs) and level else True

        if not self.right_int:
            ex = self.right.explode_nested_pairs(level=level + 1)
            if ex is False:
                return False
            elif ex is True:
                return True
            else:
                if level == 3:
                    self.right = 0
                    self.right_int = True
                return_exs = []
                for e in ex:
                    if e.direction is Direction.LEFT:
                        if self.left_int:
                            self.left += e.value
                        else:
                            self.left._add_number_from_explode(e.value, leftmost=False)
                    else:
                        return_exs.append(e)

                return return_exs if len(return_exs) and level else True
        else:
            return False

    def split_large_values(self) -> bool:
        if self.left_int:
            if self.left > 9:
                self.left = Pair(self.left // 2, int(np.ceil(self.left / 2)))
                self.left_int = False
                return True
            else:
                pass
        else:
            if self.left.split_large_values():
                return True

        if self.right_int:
            if self.right > 9:
                self.right = Pair(self.right // 2, int(np.ceil(self.right / 2)))
                self.right_int = False
                return True
            else:
                return False
        else:
            return self.right.split_large_values()

    def __add__(self, other: "Pair") -> "Pair":
        p = Pair(left=self.copy(), right=other.copy())
        p.reduce()
        return p

    @classmethod
    def from_str(cls, string: str) -> "Pair":
        assert string[0] == "["
        assert string[-1] == "]"
        _string = string[1:-1]
        if _string[0] == "[":  # Left is another pair
            open_count = 0
            for i, c in enumerate(_string):
                open_count += {"[": 1, "]": -1}.get(c, 0)
                if not open_count:
                    break
            return cls(
                cls.from_str(_string[: i + 1]),
                cls._pair_or_value(_string[i + 2 :]),
            )
        else:  # Left is a number
            left, right = _string.split(",", 1)
            return cls(int(left), cls._pair_or_value(right))

    @classmethod
    def _pair_or_value(cls, string: str) -> Union["Pair", int]:
        return int(string) if string.isnumeric() else cls.from_str(string)

    def __repr__(self) -> str:
        return f"[{self.left},{self.right}]"
