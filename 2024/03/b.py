import re

REG = re.compile("mul\(\d+,\d+\)|do\(\)|don't\(\)")


def run(inputs: str) -> int:
    total = 0
    do = True
    for match in REG.findall(inputs):
        if match == "do()":
            do = True
        elif match == "don't()":
            do = False
        elif do:
            a, b = map(int, match[4:-1].split(","))
            total += a * b
    return total
