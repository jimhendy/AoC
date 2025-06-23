from typing import TypeVar

T = TypeVar("T")


def parse_list_of_lists(inputs: list[list[T]]) -> dict[complex, T]:
    """
    Parse a list of lists into a dictionary with complex keys.

    E.g.

    [[1, 2], [3, 4]] becomes
    {
        0 + 0j: 1,
        1 + 0j: 2,
        0 + 1j: 3,
        1 + 1j: 4
    }
    """
    results = {}
    for y, row in enumerate(inputs):
        for x, value in enumerate(row):
            results[complex(x, y)] = value
    return results


def parse_grid(
    inputs: str,
    blacklist: str | list[str] | None = None,
    whitelist: str | list[str] | None = None,
) -> dict[complex, str]:
    """
    Parse a grid from a string, optionally filtering out characters.

    Args:
        inputs: The string to parse.
        blacklist: Characters to ignore.
        whitelist: Characters to include.

    Returns:
        A dictionary mapping coordinates to characters.

    """
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
