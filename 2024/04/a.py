import re
import numpy as np

TARGET = re.compile("XMAS")


def _count_targets(rows: list[str]) -> int:
    count = 0
    for row in rows:
        count += len(TARGET.findall(row))
        count += len(TARGET.findall(row[::-1]))
    return count


def _diagonals(array: np.array) -> list[str]:
    lines = ["".join(np.diag(array))]
    offset = 1
    while True:
        up_diag = np.diag(array, k=offset)
        if len(up_diag):
            lines.append("".join(up_diag))
        down_diag = np.diag(array, k=-offset)
        if len(down_diag):
            lines.append("".join(down_diag))
        if not len(up_diag) and not len(down_diag):
            break
        offset += 1
    return lines


def run(inputs: str) -> int:
    array = np.array([list(row) for row in inputs.splitlines()])

    count = 0

    # Left to right
    count += _count_targets(inputs.splitlines())

    # Top to bottom
    lines = ["".join(line) for line in array.T]
    count += _count_targets(lines)

    # Diagonals
    count += _count_targets(_diagonals(array))

    # Backwards diagonals
    count += _count_targets(_diagonals(array[::-1]))

    return count
