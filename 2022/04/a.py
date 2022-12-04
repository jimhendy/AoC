import re


def run(inputs):
    reg = re.compile(r"^(\d+)\-(\d+),(\d+)\-(\d+)$")
    total = 0
    for line in inputs.splitlines():
        min_1, max_1, min_2, max_2 = list(map(int, *reg.findall(line)))

        if min_2 < min_1:
            min_1, max_1, min_2, max_2 = min_2, max_2, min_1, max_1
        elif min_1 == min_2:
            total += 1
            continue

        total += max_2 <= max_1

    return total
