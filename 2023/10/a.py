from collections import defaultdict
from collections.abc import Iterable

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

        # for back_direction in OUTGOING_DIRECTIONS[new_grid_character]:
        #     if new_loc + back_direction == location:
        #         yield new_loc
        #         break
        if direction * -1 in OUTGOING_DIRECTIONS[new_grid_character]:
            yield new_loc


def run(inputs: str) -> int:
    grid = [list(line) for line in inputs.splitlines()]
    n_rows, n_cols = len(grid), len(grid[0])

    start = next(
        complex(x, y) for y in range(n_rows) for x in range(n_cols) if grid[y][x] == "S"
    )

    one_step_away = list(accessible_neighbours(start, grid))

    visit_record: dict[int, set[complex]] = defaultdict(set)
    visit_record[0].add(start)

    seen: set[complex] = set([start])
    steps = 0

    while one_step_away:
        steps += 1
        next_one_step_away = []

        for newly_visited_point in one_step_away:
            if newly_visited_point in seen:
                continue

            try:
                grid_character = grid[int(newly_visited_point.imag)][
                    int(newly_visited_point.real)
                ]
            except IndexError:
                continue

            if grid_character == ".":
                continue

            seen.add(newly_visited_point)
            visit_record[steps].add(newly_visited_point)

            for next_location in accessible_neighbours(newly_visited_point, grid):
                if next_location in seen:
                    continue

                next_one_step_away.append(next_location)

        one_step_away = next_one_step_away

    return max(visit_record.keys())
