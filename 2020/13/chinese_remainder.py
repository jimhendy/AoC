from functools import lru_cache

import numpy as np


def chinese_remainder(b, n):
    """
    Find the value "x" in the following system:

    x = b1 mod(n1)
    x = b2 mod(n2)
    ...
    x = bk mode(nk)

    Where n1, n2, ..., nk are co-prime
    """
    assert len(b) == len(n)
    N = np.prod(n)
    total = 0
    for ni, bi in zip(n, b):
        Ni = N / ni
        xi = inverse_mod(Ni, ni)
        total += bi * Ni * xi
    return total % N


@lru_cache(maxsize=1024)
def inverse_mod(a, n):
    """
    Return x in the below
    a * x = 1 mod(n).
    """
    reduced_a = a % n
    x = 0
    while True:
        if (reduced_a * x) % n == 1:
            return x
        x += 1
        if x > 10_000_000:
            raise RuntimeError
