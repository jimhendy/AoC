from tools.inputs import parse_grid


def _turn(direction: complex) -> complex:
    return {-1j: 1, 1: 1j, 1j: -1, -1: -1j}[direction]


def run(inputs: str) -> int:
    grid = parse_grid(inputs)
    position = next(k for k, v in grid.items() if v not in (".#"))
    if grid[position] != "^":
        raise RuntimeError("Invalid starting direction assumption")
    direction = -1j
    seen = set()
    while True:
        seen.add(position)
        next_position = position + direction
        if next_position not in grid:
            break
        while grid[next_position] == "#":
            direction = _turn(direction)
            next_position = position + direction
        position = next_position

    return len(seen)
