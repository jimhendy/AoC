import itertools

# x = real component, right +ve
# y = imag component, up +ve

WIDTH = 7
_ROCKS = [
    [complex(0, 0), complex(1, 0), complex(2, 0), complex(3, 0)],
    [complex(1, 0), complex(0, 1), complex(1, 1), complex(2, 1), complex(1, 2)],
    [complex(0, 0), complex(1, 0), complex(2, 0), complex(2, 1), complex(2, 2)],
    [complex(0, 0), complex(0, 1), complex(0, 2), complex(0, 3)],
    [complex(0, 0), complex(0, 1), complex(1, 1), complex(1, 0)],
]
ROCKS = itertools.cycle(_ROCKS)


def run(inputs):
    jet = itertools.cycle(inputs)
    occupied = set()
    highest_rock = -1

    down_offset = complex(0, -1)
    origin_x = 2
    rock_i = 0
    full_iteration_count = 0
    volume_by_rock = {}

    while True:
        origin = complex(origin_x, highest_rock + 4)
        new_rock = [p + origin for p in next(ROCKS)]

        while True:
            # Sideways
            if next(jet) == "<":
                offset = complex(-1, 0)
                new_pos = [p + offset for p in new_rock]
                if all(p.real >= 0 for p in new_pos) and all(
                    p not in occupied for p in new_pos
                ):
                    new_rock = new_pos
            else:
                offset = complex(1, 0)
                new_pos = [p + offset for p in new_rock]
                if all(p.real < WIDTH for p in new_pos) and all(
                    p not in occupied for p in new_pos
                ):
                    new_rock = new_pos

            # Downwards
            new_pos = [p + down_offset for p in new_rock]
            if all(p.imag >= 0 for p in new_pos) and all(
                p not in occupied for p in new_pos
            ):
                new_rock = new_pos
            else:
                [occupied.add(p) for p in new_rock]
                highest_rock = max(highest_rock, max(p.imag for p in new_rock))
                break

        rock_i += 1

        if not rock_i % len(_ROCKS):
            full_iteration_count += 1
            current = highest_rock
            volume_by_rock[full_iteration_count] = current
            print(volume_by_rock)
            if volume_by_rock.get(full_iteration_count / 2) == current / 2:
                print(full_iteration_count, current)
                break

    print(volume_by_rock)
    return highest_rock + 1
