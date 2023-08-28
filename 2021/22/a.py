import os


def get_extremes(numbers, variable):
    lower, upper = list(
        map(int, numbers.split(variable + "=")[1].split(",")[0].split("..")),
    )

    return [lower, upper + 1]


def run(inputs):
    on = set()

    for line in inputs.split(os.linesep):
        func = on.add if line.startswith("on ") else on.discard
        numbers = line.split()[1]
        for x in range(*get_extremes(numbers, "x")):
            if not -50 <= x <= 50:
                continue
            for y in range(*get_extremes(numbers, "y")):
                if not -50 <= y <= 50:
                    continue
                for z in range(*get_extremes(numbers, "z")):
                    if not -50 <= z <= 50:
                        continue
                    func((x, y, z))

    return len(on)
