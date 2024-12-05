from collections import defaultdict

import numpy as np
import pandas as pd

ITERATIONS = 1_000_000_000
CACHE = {}


def _step(direction: str) -> complex:
    return {
        "N": complex(0, -1),
        "S": complex(0, 1),
        "W": complex(-1, 0),
        "E": complex(1, 0),
    }[direction]


def loop_mobile_rocks(mobile_rocks: set[complex], direction: str) -> set[complex]:
    attr = "imag" if direction in "NS" else "real"

    sorted_xy = defaultdict(list)
    for mb in mobile_rocks:
        sorted_xy[getattr(mb, attr)].append(mb)

    keys = sorted(sorted_xy.keys())
    if direction in "SE":
        keys = reversed(keys)

    for xy in keys:
        for mb in sorted_xy[xy]:
            yield mb


def tilt(
    static_rocks: set[complex],
    mobile_rocks: set[complex],
    max_y: int,
    max_x: int,
    direction: str,
) -> set[complex]:
    cache_key = frozenset(mobile_rocks)
    if cache_key not in CACHE:
        movement = True
        step = _step(direction)

        while movement:
            movement = False

            new_mobile_rocks: set[complex] = set()

            for location in loop_mobile_rocks(mobile_rocks, direction):
                destination = location + step

                if not (0 <= destination.real <= max_x):
                    # Can't move off the edge
                    new_mobile_rocks.add(location)
                    continue

                if not (0 <= destination.imag <= max_y):
                    # Can't move off the edge
                    new_mobile_rocks.add(location)
                    continue

                if destination in static_rocks:
                    # Can't move into a static rock
                    new_mobile_rocks.add(location)
                    continue

                if destination in new_mobile_rocks:
                    # Can't move into another mobile rock
                    new_mobile_rocks.add(location)
                    continue

                new_mobile_rocks.add(destination)
                movement = True

            mobile_rocks = new_mobile_rocks

        CACHE[cache_key] = mobile_rocks
    return CACHE[cache_key]


def calculate_load(mobile_rocks: set[complex], max_y: int) -> int:
    load = 0
    for location in mobile_rocks:
        load += max_y - location.imag + 1
    return load


def calculate_cycle(history: dict[str, list[int]]) -> int:
    """
    Find the start, length and values of the cycle.
    """
    df = pd.DataFrame(history)
    last_line = df.iloc[-1]

    other_indices = (
        df.eq(last_line).iloc[:-1].all(axis=1).replace(False, np.nan).dropna()
    )
    for latest_cycle_start in other_indices.index[::-1]:
        print(latest_cycle_start)
        cycle_length = df.shape[0] - latest_cycle_start - 1
        if df.shape[0] < cycle_length * 2:
            break
        latest_iteration = df.iloc[-cycle_length:]
        second_latest_iteration = df.iloc[-2 * cycle_length : -cycle_length]

        if np.all(latest_iteration.values == second_latest_iteration.values):
            # Find the first cycle start
            first_cycle_start = 0
            while first_cycle_start < df.shape[0]:
                first_cycle = df.iloc[
                    first_cycle_start : first_cycle_start + cycle_length
                ]
                second_cycle = df.iloc[
                    first_cycle_start + cycle_length : first_cycle_start
                    + 2 * cycle_length
                ]
                if np.all(first_cycle.values == second_cycle.values):
                    return first_cycle_start, cycle_length, first_cycle
                first_cycle_start += 1


def run(inputs: str) -> int:
    static_rocks: set[complex] = set()
    mobile_rocks: set[complex] = set()

    max_y, max_x = 0, 0

    for y, line in enumerate(inputs.splitlines()):
        max_y = max(max_y, y)
        for x, character in enumerate(line):
            max_x = max(max_x, x)
            if character == "#":
                static_rocks.add(complex(x, y))
            elif character == "O":
                mobile_rocks.add(complex(x, y))

    directions = "NWSE"
    history = defaultdict(list)
    for _ in range(ITERATIONS):
        for dir in directions:
            mobile_rocks = tilt(
                static_rocks,
                mobile_rocks,
                max_y=max_y,
                max_x=max_x,
                direction=dir,
            )
            history[dir].append(calculate_load(mobile_rocks, max_y=max_y))

        if not _ % 10:
            cycle_data = calculate_cycle(history)
            if cycle_data is not None:
                break

    cycle_start, cycle_length, cycle_values = cycle_data

    cycle_iterations = ITERATIONS - cycle_start
    remaining_iterations = cycle_iterations % cycle_length

    return cycle_values["E"].iloc[remaining_iterations - 1]
