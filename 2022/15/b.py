import re

import numba as nb
import numpy as np

REG_NUM = r"(-?\d+)"
REG = re.compile(
    f"^Sensor at x={REG_NUM}, y={REG_NUM}: closest beacon is at x={REG_NUM}, y={REG_NUM}$",
)

# Range = 1D np.ndarray with 2 element, lower and upper
Range = np.ndarray
INT = np.int64  # Bigger than MAX


@nb.njit("i8(i8[:])", boundscheck=False, cache=True)
def lower(range_: Range) -> INT:
    return range_[0]


@nb.njit("i8(i8[:])", boundscheck=False, cache=True)
def upper(range_: Range) -> INT:
    return range_[1]


@nb.njit("b1(i8[:], i8[:])", boundscheck=False, cache=True)
def ranges_overlap(range_1: Range, range_2: Range) -> bool:
    left = range_1 if lower(range_1) < lower(range_2) else range_2
    right = range_1 if range_2 is left else range_2
    # As this grid is all integers, lets say two ranges overlap if they touch
    return lower(left) <= upper(right) and (lower(right) - 1) <= upper(left)


@nb.njit("i8(i8[:,:], i8)", parallel=False, boundscheck=False, cache=True)
def numba_run(inputs: np.ndarray, grid_size: INT) -> INT:
    distances = np.zeros(inputs.shape[0], dtype=INT)

    for sensor_id in nb.prange(inputs.shape[0]):
        sx, sy, bx, by = inputs[sensor_id]
        distances[sensor_id] = abs(bx - sx) + abs(by - sy)

    for Y in range(grid_size + 1):
        ranges = []
        for sensor_id in range(inputs.shape[0]):
            sensor_x = inputs[sensor_id, 0]
            sensor_y = inputs[sensor_id, 1]

            dist_to_Y = abs(Y - sensor_y)
            width_at_y = distances[sensor_id] - dist_to_Y

            if width_at_y > 0:
                min_x = sensor_x - width_at_y
                max_x = sensor_x + width_at_y

                min_x = max(min_x, 0)

                max_x = min(max_x, grid_size)

                ranges.append(np.array([min_x, max_x]))

        while True:
            combined = False
            for i, ri in enumerate(ranges):
                for j, rj in enumerate(ranges):
                    if i == j:
                        continue
                    if ranges_overlap(ri, rj):
                        ranges.pop(j)
                        ri[0] = min(lower(ri), lower(rj))
                        ri[1] = max(upper(ri), upper(rj))

                        combined = True
                        break
                if combined:
                    break
            if not combined:
                break

        if len(ranges) != 1:
            for r in ranges:
                if lower(r) == 0:
                    return 4_000_000 * (upper(r) + 1) + Y

    return 0


def run(inputs):
    inputs = np.array(
        [list(map(int, REG.findall(line)[0])) for line in inputs.splitlines()],
        dtype=INT,
    )

    return numba_run(inputs, 4_000_000)
