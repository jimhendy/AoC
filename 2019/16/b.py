import numba
import numpy as np


@numba.njit
def run_phase(inp):
    output = np.zeros(len(inp))
    for i, x in enumerate(inp[::-1]):
        output[-i - 1] = (output[-i] + x) % 10
    return output


def run(inputs):
    offset = int(inputs[:7])
    data = list(inputs) * 10000

    # If this is the case then we only care about the cumulative sum
    """
    The top half of the matrix is complicated to compute but the lower right
    is simply the cumsum of the values and "luckily" the offset means
    we only care about the lower right corner
    """
    assert offset > len(data) / 2

    data = list(map(int, data[offset:]))

    for _i in range(100):
        data = run_phase(data)

    return "".join(map(str, map(int, data[:8])))
