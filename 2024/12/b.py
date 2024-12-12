from collections import defaultdict

from tools.inputs import parse_grid


def find_all_regions(
    grid: dict[complex, str],
    *,
    do_not_cross_lines: bool = False,
) -> list[set[complex]]:
    seen: set[complex] = set()
    regions: list[set[complex]] = []
    for loc in grid:
        if loc in seen:
            continue
        char = grid[loc]
        region = set()
        stack = [loc]
        while stack:
            loc = stack.pop()
            if loc in seen or loc not in grid or grid[loc] != char:
                continue
            seen.add(loc)
            region.add(loc)
            steps = []
            if int(loc.real) == loc.real:
                steps.extend([1, -1])
            if int(loc.imag) == loc.imag:
                steps.extend([1j, -1j])
            for d in steps:
                new_loc = loc + d
                if do_not_cross_lines:
                    if d.real == 1:
                        boundry_offsets = [0.5 + 0.5j, 0.5 - 0.5j]
                    elif d.real == -1:
                        boundry_offsets = [-0.5 + 0.5j, -0.5 - 0.5j]
                    elif d.imag == 1:
                        boundry_offsets = [0.5 + 0.5j, -0.5 + 0.5j]
                    elif d.imag == -1:
                        boundry_offsets = [0.5 - 0.5j, -0.5 - 0.5j]
                    else:
                        raise ValueError(f"Invalid direction {d}")
                    if all(loc + offset in grid for offset in boundry_offsets):
                        continue
                stack.append(new_loc)
        regions.append(region)
    return regions


def find_sides(region: set[complex]) -> int:
    """
    Sum the number of unique edges in the region
    """
    edges = defaultdict(int)
    for c in region:
        left = c - 0.5
        right = c + 0.5
        up = c + 0.5j
        down = c - 0.5j
        for d in [left, right, up, down]:
            edges[d] += 1

    perimeter = {k: "A" for k, v in edges.items() if v == 1}

    sides = find_all_regions(perimeter, do_not_cross_lines=True)
    return len(sides)


def run(inputs: str) -> int:
    grid: dict[complex, str] = parse_grid(inputs)
    regions: list[set[complex]] = find_all_regions(grid)

    total = 0
    for region in regions:
        area = len(region)
        sides: int = find_sides(region)
        total += area * sides

    return total
