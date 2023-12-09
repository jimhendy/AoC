from functools import lru_cache

import numpy as np


def chinese_remainder(b: np.ndarray, n: np.ndarray) -> int:
    """
    Find the value "x" in the following system:

    x = b1 mod(n1)
    x = b2 mod(n2)
    ...
    x = bk mode(nk)

    Where n1, n2, ..., nk are co-prime
    """
    if len(b) != len(n):
        error = f"b and n must have the same length, got {len(b)=} and {len(n)=}"
        raise ValueError(error)
    n_ = np.prod(n)
    total = 0
    for ni, bi in zip(n, b, strict=True):
        ni_ = n_ / ni
        xi = inverse_mod(ni_, ni)
        total += bi * ni_ * xi
    return total % n_


@lru_cache(maxsize=1024)
def inverse_mod(a: int, n: int) -> int:
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
