from tools.inputs import parse_grid
from collections import defaultdict
from itertools import combinations


def antinode(a: complex, b: complex) -> complex:
    """
    The point twice as far from a as b, in the same direction as b.

    Such that:
    abs(antinode - a) * 2 == abs(antinode - b)
    """
    return b + (b - a)


def run(inputs: str) -> int:
    grid: dict[complex:str] = parse_grid(inputs)
    char_to_locs = defaultdict(list)
    for loc, char in grid.items():
        if char == ".":
            continue
        char_to_locs[char].append(loc)

    antinodes = set()
    for char, locs in char_to_locs.items():
        for a, b in combinations(locs, 2):
            if (node := antinode(a, b)) in grid:
                antinodes.add(node)
            if (node := antinode(b, a)) in grid:
                antinodes.add(node)
    return len(antinodes)
