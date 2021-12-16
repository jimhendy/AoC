import os
import re


def run(inputs):

    reg = re.compile(r"(\w+) ([-+]?\d*\.?\d+)")
    horizontal, depth, aim = 0, 0, 0

    for line in inputs.split(os.linesep):

        direction, value = reg.findall(line)[0]
        value = int(value)

        if direction == "forward":
            horizontal += value
            depth += aim * value
        elif direction == "up":
            aim -= value
        elif direction == "down":
            aim += value
        else:
            raise NotImplementedError(f'Unexpected command: "{line}"')

    return horizontal * depth
