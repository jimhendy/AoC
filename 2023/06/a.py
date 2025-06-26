import numpy as np


def run(inputs: str) -> int:
    """Number of ways we can beat the record.

    Distance = Speed * Time
    -
    Speed = Changing time = x
    Time = Total time - Chanrging Time = T - x
    -
    Distance = x * (T-x) = - x^2 + T*x
    -
    Record_distance = R = - x^2 + T*x
    0 = - x^2 + T*x + R
    -
    Roots of the above show charging times that match record_distance
    """
    total = 1
    times, distances = (iter(line.split()) for line in inputs.splitlines())
    # Get rid of the titles
    next(times), next(distances)

    for time, record_distance in zip(map(int, times), map(int, distances), strict=True):
        roots = np.roots([-1, time, -record_distance - 1e-5])

        if len(roots) == 2 and all(np.isreal(x) for x in roots):
            lower = min(roots)
            upper = max(roots)

            if int(lower) == lower:
                lower += 1

            if int(upper) == upper:
                upper -= 1

            lower = np.ceil(lower)
            upper = np.floor(upper)

            span = upper - lower + 1

            total *= span

    return total
