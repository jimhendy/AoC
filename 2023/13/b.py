import numpy as np


class PivotError(Exception):
    pass


def potential_pivots(pattern: np.ndarray) -> np.ndarray:
    """
    Indices of potential pivot points.

    These are found from consecutive differences in rows.
    The differences are absolute values and summed to
    find the total change in each row.

    Locations where the summed change is zero are
    potential pivot points.
    """
    row_deltas = np.abs(np.diff(pattern, axis=0))
    row_sums = np.sum(row_deltas, axis=1)
    pivot_indices = np.where(row_sums == 0)[0]

    return pivot_indices + 1


def find_pivot(
    pattern: np.ndarray,
    original_pivot: int | None = None,
    transpose: bool = False,
) -> int:
    """
    Find the first pivot point in the pattern.
    """
    if transpose:
        pattern = pattern.T
        if original_pivot is not None:
            original_pivot = -original_pivot

    for pivot in potential_pivots(pattern):
        if pivot == original_pivot:
            continue

        before = pattern[:pivot]
        after = pattern[pivot:]

        # Truncate the sub-patterns to the same length
        sub_pattern_length = min(len(before), len(after))
        before = before[-sub_pattern_length:]
        after = after[:sub_pattern_length]
        after = np.flip(after, axis=0)

        if np.equal(before, after).all():
            return pivot


def pivot_point(pattern: np.ndarray, original_pivot: int | None = None) -> int:
    """
    Find the poivot point for this pattern.

    Positive pivots are rows, negative are columns.
    """
    if (pivot := find_pivot(pattern, original_pivot)) is not None:
        return pivot
    if (pivot := find_pivot(pattern, original_pivot, transpose=True)) is not None:
        return pivot * -1

    raise PivotError(f"No pivot found for {pattern=}")


def alternate_pivot_point(pattern: np.ndarray, original_pivot: int) -> int:
    for y, line in enumerate(pattern):
        for x, value in enumerate(line):
            new_pattern = pattern.copy()
            if value == 1:
                new_pattern[y, x] = 0
            else:
                new_pattern[y, x] = 1

            try:
                return pivot_point(new_pattern, original_pivot=original_pivot)
            except PivotError:
                pass

    raise PivotError(f"No alternate pivot found for \n{pattern}")


def run(inputs: str) -> int:
    total = 0

    for pattern_list in inputs.split("\n\n"):
        pattern = np.array(
            [
                [character == "#" for character in line]
                for line in pattern_list.splitlines()
            ],
            dtype=int,
        )

        original_pivot = pivot_point(pattern)

        alternate = alternate_pivot_point(pattern, original_pivot)
        if alternate > 0:
            total += 100 * alternate
        else:
            total += -1 * alternate

    return total
