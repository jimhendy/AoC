import re

REG = re.compile(r"mul\(\d+,\d+\)")


def run(inputs: str) -> int:
    total = 0
    for match in REG.findall(inputs):
        a, b = map(int, match[4:-1].split(","))
        total += a * b
    return total
