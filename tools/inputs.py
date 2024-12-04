def parse_grid(
    inputs: str,
    ignore_chars: str | list[str] | None = None,
) -> dict[complex, str]:
    if isinstance(ignore_chars, str):
        ignore_chars = [ignore_chars]

    grid = {}
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            if ignore_chars and c in ignore_chars:
                continue
            grid[complex(x, y)] = c

    return grid


def nb4(location: complex) -> list[complex]:
    return [location + step for step in [1, -1, 1j, -1j]]


def nb8(location: complex) -> list[complex]:
    return [
        location + step for step in [1, -1, 1j, -1j, 1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]
    ]
