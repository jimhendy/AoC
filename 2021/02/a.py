import os
import re


def run(inputs):

    reg = re.compile(r"(\w+) ([-+]?\d*\.?\d+)")
    horizontal, depth = 0, 0

    for line in inputs.split(os.linesep):

        direction, value = reg.findall(line)[0]
        value = int(value)

        if direction == "forward":
            horizontal += value
        elif direction == "up":
            depth -= value
        elif direction == "down":
            depth += value
        else:
            raise NotImplementedError(f'Unexpected command: "{line}"')

    return horizontal * depth