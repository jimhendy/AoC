import os
import re


def run(inputs):
    reg = re.compile(r"(\d+)\-(\d+) ([a-zA-Z])\: ([a-zA-Z]+)")
    total = 0
    for l in inputs.split(os.linesep):
        match = reg.findall(l)[0]
        first = match[3][int(match[0]) - 1] == match[2]
        second = match[3][int(match[1]) - 1] == match[2]
        if first + second == 1:
            total += 1

    return total
