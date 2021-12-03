from typing import Iterable

def binary_to_decimal(binary_array: Iterable[int]) -> int:
    """
    Find the decimal representation of a binary number.

    E.g.

    binary_to_decimal([1, 0, 1]) -> 5

    :param binary_array: 1-dimentsional iterable of ones and zeros to convert
    :return: Integer decimal number
    """
    return int(''.join(map(str, binary_array)), base=2)
