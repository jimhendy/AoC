def parse_grid(
    inputs: str,
    blacklist: str | list[str] | None = None,
    whitelist: str | list[str] | None = None,
) -> dict[complex, str]:
    if blacklist and whitelist:
        msg = "Cannot have both a blacklist and a whitelist"
        raise ValueError(msg)

    if isinstance(blacklist, str):
        blacklist = [blacklist]
    if isinstance(whitelist, str):
        whitelist = [whitelist]

    grid = {}
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            if blacklist and c in blacklist:
                continue
            if whitelist and c not in whitelist:
                continue
            grid[complex(x, y)] = c

    return grid


def loc_in_grid(inputs: str, character: str) -> complex:
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            if c == character:
                return complex(x, y)
    msg = f"Character {character} not found in grid"
    raise ValueError(msg)


def nb4(location: complex) -> list[complex]:
    return [location + step for step in [1, -1, 1j, -1j]]


def nb8(location: complex) -> list[complex]:
    return [
        location + step for step in [1, -1, 1j, -1j, 1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]
    ]
