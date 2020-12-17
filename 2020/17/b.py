import os
import re


def extreme_cubes(active):
    min_x, min_y, min_z, min_w, max_x, max_y, max_z, max_w = 0, 0, 0, 0, 0, 0, 0, 0
    for x, y, z, w in active:
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
        if z > max_z:
            max_z = z
        if w > max_w:
            max_w = w
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
        if z < min_z:
            min_z = z
        if w < min_w:
            min_w = w
    return min_x, min_y, min_z, min_w, max_x, max_y, max_z, max_w


def nb80(cube):
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for dw in (-1, 0, 1):
                    if not dx and not dy and not dz and not dw:
                        continue
                    yield (cube[0] + dx, cube[1] + dy, cube[2] + dz, cube[3] + dw)


def cycle(active):
    active_pre_cycle = active.copy()
    min_x, min_y, min_z, min_w, max_x, max_y, max_z, max_w = extreme_cubes(active)
    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            for z in range(min_z - 1, max_z + 2):
                for w in range(min_w - 1, max_w + 2):
                    cube = (x, y, z, w)
                    is_active = cube in active_pre_cycle
                    n_active = 0
                    for n in nb80(cube):
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
    w = 0

    for y, line in enumerate(inputs.split(os.linesep)):
        for x, char in enumerate(line):
            if char == "#":
                active.add((x, y, z, w))

    [cycle(active) for _ in range(6)]

    return len(active)