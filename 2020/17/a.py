import os


def extreme_cubes(active):
    min_x, min_y, min_z, max_x, max_y, max_z = 0, 0, 0, 0, 0, 0
    for x, y, z in active:
        max_x = max(x, max_x)
        max_y = max(y, max_y)
        max_z = max(z, max_z)
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        min_z = min(z, min_z)
    return min_x, min_y, min_z, max_x, max_y, max_z


def nb26(cube):
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if not dx and not dy and not dz:
                    continue
                yield (cube[0] + dx, cube[1] + dy, cube[2] + dz)


def cycle(active):
    active_pre_cycle = active.copy()
    min_x, min_y, min_z, max_x, max_y, max_z = extreme_cubes(active)
    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            for z in range(min_z - 1, max_z + 2):
                cube = (x, y, z)
                is_active = cube in active_pre_cycle
                n_active = 0
                for n in nb26(cube):
                    n_active += n in active_pre_cycle
                    if n_active > 3:
                        break
                if is_active and (n_active != 2 and n_active != 3):
                    active.remove(cube)
                elif not is_active and n_active == 3:
                    active.add(cube)


def run(inputs):
    active = set()
    z = 0

    for y, line in enumerate(inputs.split(os.linesep)):
        for x, char in enumerate(line):
            if char == "#":
                active.add((x, y, z))

    [cycle(active) for _ in range(6)]

    return len(active)
