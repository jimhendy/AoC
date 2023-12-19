from collections import defaultdict


def run(inputs: str) -> int:
    static_rocks: dict[int, set[int]] = defaultdict(set)
    mobile_rocks: dict[int, set[int]] = defaultdict(set)

    max_y = 0

    for y, line in enumerate(inputs.splitlines()):
        max_y = max(max_y, y)
        for x, character in enumerate(line):
            if character == "#":
                static_rocks[y].add(x)
            elif character == "O":
                mobile_rocks[y].add(x)

    movement = True

    while movement:
        movement = False

        new_mobile_rocks: dict[int, set[int]] = defaultdict(set)

        y_values_with_mobile_rocks = sorted(mobile_rocks.keys())

        for y in y_values_with_mobile_rocks:
            row_mobile_rocks = mobile_rocks[y]

            if not y:
                # Can't fall off the top edge
                new_mobile_rocks[y].update(row_mobile_rocks)
                continue

            destination_y = y - 1

            for x in row_mobile_rocks:
                if x in static_rocks[destination_y]:
                    # Can't move into a static rock
                    new_mobile_rocks[y].add(x)
                    continue

                if x in mobile_rocks[destination_y]:
                    # Can't move into another mobile rock
                    new_mobile_rocks[y].add(x)
                    continue

                new_mobile_rocks[destination_y].add(x)
                movement = True

        mobile_rocks = new_mobile_rocks

    load = 0
    for y, row_mobile_rocks in mobile_rocks.items():
        load += (max_y - y + 1) * len(row_mobile_rocks)

    return load
