from collections.abc import Iterable

from matplotlib.path import Path

OUTGOING_DIRECTIONS = {
    "|": (complex(0, 1), complex(0, -1)),
    "-": (complex(1, 0), complex(-1, 0)),
    "L": (complex(0, -1), complex(1, 0)),
    "J": (complex(0, -1), complex(-1, 0)),
    "7": (complex(0, 1), complex(-1, 0)),
    "F": (complex(0, 1), complex(1, 0)),
    "S": (complex(0, 1), complex(0, -1), complex(1, 0), complex(-1, 0)),
    ".": tuple(),
}


def accessible_neighbours(
    location: complex,
    grid: list[list[str]],
) -> Iterable[complex]:
    try:
        grid_character = grid[int(location.imag)][int(location.real)]
    except IndexError:
        raise StopIteration

    for direction in OUTGOING_DIRECTIONS[grid_character]:
        new_loc = location + direction

        try:
            new_grid_character = grid[int(new_loc.imag)][int(new_loc.real)]
        except IndexError:
            continue

        if direction * -1 in OUTGOING_DIRECTIONS[new_grid_character]:
            yield new_loc


def run(inputs: str) -> int:
    grid = [list(line) for line in inputs.splitlines()]
    n_rows, n_cols = len(grid), len(grid[0])

    location = next(
        complex(x, y) for y in range(n_rows) for x in range(n_cols) if grid[y][x] == "S"
    )

    main_loop: list[complex] = []
    seen: set[complex] = set()

    while location not in main_loop:
        main_loop.append(location)
        seen.add(location)

        updated = False

        for next_location in accessible_neighbours(location, grid):
            if next_location in seen:
                continue
            location = next_location
            updated = True
            break

        if not updated:
            break

    loop_path = Path([[int(x.real), int(x.imag)] for x in main_loop])

    internal = 0
    for y in range(n_rows):
        for x in range(n_cols):
            if complex(x, y) in main_loop:
                continue
            elif loop_path.contains_point([x, y]):
                internal += 1

    return internal
