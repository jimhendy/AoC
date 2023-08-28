import itertools

# x = real component, right +ve
# y = imag component, up +ve

WIDTH = 7
ROCKS = itertools.cycle(
    [
        [complex(0, 0), complex(1, 0), complex(2, 0), complex(3, 0)],
        [complex(1, 0), complex(0, 1), complex(1, 1), complex(2, 1), complex(1, 2)],
        [complex(0, 0), complex(1, 0), complex(2, 0), complex(2, 1), complex(2, 2)],
        [complex(0, 0), complex(0, 1), complex(0, 2), complex(0, 3)],
        [complex(0, 0), complex(0, 1), complex(1, 1), complex(1, 0)],
    ],
)


def run(inputs):
    jet = itertools.cycle(inputs)
    occupied = set()
    highest_rock = -1

    down_offset = complex(0, -1)
    origin_x = 2

    for _ in range(2022):
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
                highest_rock = max(highest_rock, *(p.imag for p in new_rock))
                break

    return highest_rock + 1
