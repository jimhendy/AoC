import numpy as np
from collections import defaultdict


def _get_char(array: np.ndarray, location: complex) -> str:
    x = int(location.real)
    y = int(location.imag)
    if 0 <= y < array.shape[0] and 0 <= x < array.shape[1]:
        return array[y, x]
    return ""


def _count_mas(
    array: np.ndarray, a_locations: dict[complex, int], offset: complex
) -> None:
    for y, line in enumerate(array):
        for x, char in enumerate(line):
            if char == "M":
                loc = complex(x, y)
                if (
                    _get_char(array, loc + offset) == "A"
                    and _get_char(array, loc + 2 * offset) == "S"
                ):
                    a_locations[loc + offset] += 1


def run(inputs: str) -> int:
    array = np.array([list(row) for row in inputs.splitlines()])

    a_locations = defaultdict(int)
    _count_mas(array, a_locations, 1 + 1j)
    _count_mas(array, a_locations, 1 - 1j)
    _count_mas(array, a_locations, -1 + 1j)
    _count_mas(array, a_locations, -1 - 1j)

    valid = len([loc for loc, count in a_locations.items() if count == 2])

    return valid
