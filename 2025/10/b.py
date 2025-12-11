import re

import cvxpy as cp

REGEX = re.compile(
    r"\[(?P<lights>[.#]+)\](?P<buttons>(?: \([0-9,]+\))+?) \{(?P<aim>[0-9, ]+)\}",
)


def run(input: str) -> int:
    total = 0
    for line in input.splitlines():
        print(f"Processing line: {line}")
        match = REGEX.match(line)

        if not match:
            msg = f"Line does not match expected format: {line}"
            raise ValueError(msg)

        buttons_str = match.group("buttons").strip().split(" ")
        aim_str = match.group("aim")

        buttons = tuple(
            tuple(sorted(map(int, b[1:-1].split(",")))) for b in buttons_str
        )
        aim = tuple(map(int, aim_str.split(",")))

        n = len(aim)
        m = len(buttons)
        x = cp.Variable(
            m, integer=True, nonneg=True,
        )  # Number of times to press each button
        constraints = []
        for i in range(n):
            coeffs = [1 if i in buttons[j] else 0 for j in range(m)]
            constraints.append(cp.sum(cp.multiply(coeffs, x)) == aim[i])
        problem = cp.Problem(cp.Minimize(cp.sum(x)), constraints)

        problem.solve()
        if problem.status != cp.OPTIMAL:
            msg = f"Could not find optimal solution for line: {line}"
            raise ValueError(msg)
        total += x.value.sum()

    return total
