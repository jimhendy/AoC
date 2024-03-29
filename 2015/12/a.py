import re


def run(inputs):
    num_reg = re.compile(r"(-?\d+)")

    total = 0
    for n in num_reg.findall(inputs):
        total += int(n)

    return total
