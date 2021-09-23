import os


def run(inputs):
    total = 0
    for line in inputs.split(os.linesep):
        total += int(line)
    return total
