from collections import defaultdict

from tools.inputs import parse_grid


def find_all_regions(grid: dict[complex, str]) -> list[set[complex]]:
    seen: set[complex] = set()
    y_max = max(int(c.imag) for c in grid)
    x_max = max(int(c.real) for c in grid)
    regions: list[set[complex]] = []
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            c = complex(x, y)
            if c in seen:
                continue
            char = grid[c]
            region = set()
            stack = [c]
            while stack:
                c = stack.pop()
                if c in seen or c not in grid or grid[c] != char:
                    continue
                seen.add(c)
                region.add(c)
                for d in [1, -1, 1j, -1j]:
                    stack.append(c + d)
            regions.append(region)
    return regions


def find_perimeter(region: set[complex]) -> int:
    """Sum the number of unique edges in the region"""
    edges = defaultdict(int)
    for c in region:
        left = c - 0.5
        right = c + 0.5
        up = c + 0.5j
        down = c - 0.5j
        for d in [left, right, up, down]:
            edges[d] += 1
    return len([k for k, v in edges.items() if v == 1])


def run(inputs: str) -> int:
    grid: dict[complex, str] = parse_grid(inputs)
    regions: list[set[complex]] = find_all_regions(grid)

    total = 0
    for region in regions:
        area = len(region)
        permieter: int = find_perimeter(region)
        total += area * permieter

    return total
