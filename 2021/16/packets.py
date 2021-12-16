from abc import ABC, abstractmethod
import numpy as np

from typing import List
from tools.number_conversion import binary_to_decimal


class Packet(ABC):
    """
    Abstract base class for a Packet from the hex-message queue.
    """

    def __init__(self, version: int, type_id: int):
        self.version = version
        self.type_id = type_id
        self._cached_value = None

    def value(self) -> int:
        """
        Fetch the value of this packet. Values are cached to streamline complex calculations.
        """
        if self._cached_value is None:
            self._cached_value = self._value()
        return self._cached_value

    @abstractmethod
    def _value(self):
        pass


class Literal(Packet):
    """
    A literal ``Packet`` (``type_id=4``).

    This packet represents a numerical value only.
    """

    def __init__(self, version: int, binary: List[str]):
        super().__init__(version=version, type_id=4)
        self.binary = binary
        self.decimal = binary_to_decimal(self.binary)

    def _value(self) -> int:
        return self.decimal


class Operator(Packet):
    """
    An operator ``Packet``.

    This packet represents a calculation on ``Literals``.
    """

    def __init__(self, version: int, type_id: int, subpackets: List[Packet]):
        assert type_id != 4
        super().__init__(version=version, type_id=type_id)
        self.subpackets = subpackets

    def _value(self) -> int:
        sub_values = [sp.value() for sp in self.subpackets]

        if self.type_id in {5, 6, 7}:
            assert len(sub_values) == 2

        func = {
            0: sum,
            1: np.prod,
            2: min,
            3: max,
            5: lambda x: int(x[0] > x[1]),
            6: lambda x: int(x[0] < x[1]),
            7: lambda x: int(x[0] == x[1]),
        }[self.type_id]

        return func(sub_values)
