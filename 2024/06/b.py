from tools.inputs import parse_grid


def _turn(direction: complex) -> complex:
    return {-1j: 1, 1: 1j, 1j: -1, -1: -1j}[direction]


def causes_loop(
    grid: dict[complex, str], position: complex, direction: complex
) -> bool:
    seen = set()
    while True:
        if (position, direction) in seen:
            return True
        seen.add((position, direction))
        next_position = position + direction
        if next_position not in grid:
            return False
        while grid[next_position] == "#":
            direction = _turn(direction)
            next_position = position + direction
        position = next_position
    return False


def run(inputs: str) -> int:
    grid = parse_grid(inputs)
    position = next(k for k, v in grid.items() if v not in (".#"))
    if grid[position] != "^":
        raise RuntimeError("Invalid starting direction assumption")
    direction = -1j

    total = 0

    grid_width = int(max(p.real for p in grid)) + 1
    grid_height = int(max(p.imag for p in grid)) + 1

    for y in range(grid_height):
        for x in range(grid_width):
            rock_position = x + y * 1j
            if grid[rock_position] != ".":
                continue
            new_grid = grid.copy()
            new_grid[rock_position] = "#"
            if causes_loop(new_grid, position, direction):
                total += 1

    return total
