import tqdm

from tools.inputs import parse_grid


def _turn(direction: complex) -> complex:
    return {-1j: 1, 1: 1j, 1j: -1, -1: -1j}[direction]


@profile
def causes_loop(
    grid: dict[complex, str],
    position: complex,
    direction: complex,
    *,
    return_route: bool = False,
) -> bool | set[complex]:
    seen = set()
    while True:
        key = (position, direction)
        if key in seen:
            return True
        seen.add(key)
        next_position = position + direction
        if next_position not in grid:
            if return_route:
                return {s[0] for s in seen}
            return False
        while grid[next_position] == "#":
            direction = _turn(direction)
            next_position = position + direction
        position = next_position
    return False


@profile
def run(inputs: str) -> int:
    grid = parse_grid(inputs)
    position = next(k for k, v in grid.items() if v not in (".#"))
    if grid[position] != "^":
        raise RuntimeError("Invalid starting direction assumption")
    direction = -1j

    total = 0

    original_route = causes_loop(grid, position, direction, return_route=True)

    for location in tqdm.tqdm(original_route):
        x = location.real
        y = location.imag
        rock_position = x + y * 1j
        if grid[rock_position] != ".":
            continue
        new_grid = grid.copy()
        new_grid[rock_position] = "#"
        if causes_loop(new_grid, position, direction):
            total += 1

    return total
