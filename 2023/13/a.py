import numpy as np


def potential_pivots(pattern: np.ndarray) -> np.ndarray:
    """Indices of potential pivot points.

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


def find_pivot(pattern: np.ndarray) -> int:
    """Find the first pivot point in the pattern."""
    pivots = potential_pivots(pattern)
    for pivot in pivots:
        before = pattern[:pivot]
        after = pattern[pivot:]

        # Truncate the sub-patterns to the same length
        sub_pattern_length = min(len(before), len(after))
        before = before[-sub_pattern_length:]
        after = after[:sub_pattern_length]
        after = np.flip(after, axis=0)

        if np.equal(before, after).all():
            print(pivot)
            return pivot


def run(inputs: str) -> int:
    total = 0

    for i, pattern_list in enumerate(inputs.split("\n\n")):
        if i != 66:
            continue
        pattern = np.array(
            [
                [character == "#" for character in line]
                for line in pattern_list.splitlines()
            ],
            dtype=int,
        )
        if (pivot := find_pivot(pattern)) is not None:
            total += 100 * pivot
            continue

        pattern = pattern.T
        total += find_pivot(pattern)

    return total
