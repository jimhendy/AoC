from typing import Iterable, List


def binary_to_decimal(binary_array: Iterable[int]) -> int:
    """
    Find the decimal representation of a binary number.

    E.g.

    binary_to_decimal([1, 0, 1]) -> 5

    :param binary_array: 1-dimentsional iterable of ones and zeros to convert
    :return: Integer decimal number
    """
    return int("".join(map(str, binary_array)), base=2)


def hex_to_decimal(h: str) -> int:
    """
    Convert a hex character to a decimal number.

    :param h: A hex character 0->F.
    :return: Decimal representation of ``h``.
    """
    assert h in list("0123456789ABCDEF")
    return int(h, base=16)


def decimal_to_binary(d: int) -> List[str]:
    """
    Convert a decimal number to binary.

    :param d: Input decimal number.
    :return: List of binary ``str`` characters ('0' or '1')
    """
    return list("{:04d}".format(int(bin(d)[2:])))


def hex_to_binary(h: str) -> int:
    """
    Convert a hexidecimal number to its binary representation.

    :param h: Single character ``str`` of a hex number.
    :return: List of binary ``str`` characters ('0' or '1')
    """
    return decimal_to_binary(hex_to_decimal(h))
