import matplotlib.pyplot as plt
import numpy as np

from tools.binary_search import binary_search

CACHE = {}


def feul_to_dest(dest: int, initial_positions: np.ndarray) -> int:
    """
    Calculate the fuel required for all our crabby friends to travel from
    their ``initial_positions`` to ``dest``. Results are cached in ``CACHE``.

    :param dest: Horizontal destination position.
    :param initial_positions: Starting positions of all crab subs.
    :return: Feul required for this journey.
    """
    global CACHE
    if dest not in CACHE:
        diff = np.abs(initial_positions - dest)
        feul = np.multiply(diff, diff + 1).sum() / 2
        CACHE[dest] = feul
    return CACHE[dest]


def run(inputs):
    pos = np.array(inputs.split(",")).astype(int)

    def func(dest: int) -> bool:
        """
        For use in binary search to give monotonic result looking for the
        smallest value of ``dest`` where the feul required to travel to
        ``dest`` is less than the feul required to travel to ``dest + 1``.

        This will find the minimum iff:
            * The feul required is a smooth function with no noise
            * The optimum ``dest`` is not the minimum crab position

        :param dest: Horizontal position to test
        :return: Boolean of whether the (feul to dest) < (feul to dest + 1).
        """
        return feul_to_dest(dest, pos) < feul_to_dest(dest + 1, pos)

    optimum_dest = binary_search(func, lower=pos.min(), upper=pos.max())

    return CACHE[optimum_dest]
