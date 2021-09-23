import os


def run(inputs):
    inputs = inputs.split(os.linesep)
    right = 3
    down = 1
    return sum(
        [
            inputs[row][col % len(inputs[0])] == "#"
            for row, col in zip(range(0, len(inputs), down), range(0, int(9e99), right))
        ]
    )
