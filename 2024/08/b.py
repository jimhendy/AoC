import math
from collections import defaultdict
from itertools import combinations

from tools.inputs import parse_grid


def antinode(
    a: complex,
    b: complex,
    grid_width: int,
    grid_height: int,
) -> list[complex]:
    """All points from a in the direction that lie on integer coordinates."""
    unnormalised_step = b - a
    # If the unnormalised step has a common factor, we can reduce it.
    common_factor = math.gcd(int(unnormalised_step.real), int(unnormalised_step.imag))
    step = unnormalised_step / common_factor
    points = []
    current = a
    while 0 <= current.real < grid_width and 0 <= current.imag < grid_height:
        points.append(current)
        current += step
    return points


def run(inputs: str) -> int:
    grid: dict[complex:str] = parse_grid(inputs)
    char_to_locs = defaultdict(list)
    for loc, char in grid.items():
        if char == ".":
            continue
        char_to_locs[char].append(loc)

    grid_width = int(max(p.real for p in grid)) + 1
    grid_height = int(max(p.imag for p in grid)) + 1

    antinodes = set()
    for char, locs in char_to_locs.items():
        for a, b in combinations(locs, 2):
            antinodes.update(antinode(a, b, grid_width, grid_height))
            antinodes.update(antinode(b, a, grid_width, grid_height))
    return len(antinodes)
