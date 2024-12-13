import re
import numpy as np

# Button A: X+79, Y+87
BUTTON_REG = re.compile("^Button \w: X(.+), Y(.+)$")
# Prize: X=7384, Y=4824
PRICE_REG = re.compile("^Prize: X=(.+), Y=(.+)$")

TOKENS = np.array([3, 1])


def run(inputs: str) -> int:
    total = 0

    for task in inputs.split("\n\n"):
        task_lines = task.split("\n")
        ax, ay = list(map(int, BUTTON_REG.findall(task_lines[0])[0]))
        bx, by = list(map(int, BUTTON_REG.findall(task_lines[1])[0]))
        px, py = list(map(int, PRICE_REG.findall(task_lines[2])[0]))

        A = np.array([[ax, ay], [bx, by]]).T
        x = np.array([px, py])

        loc = np.linalg.solve(A, x)

        if np.allclose(loc, np.round(loc)):
            total += TOKENS @ np.abs(loc)

    return total
