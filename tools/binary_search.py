import logging

from tools.errors import BinarySearchError

DEBUG = False


logger = logging.getLogger(__name__)

_MAX_UPPER_FIND_ITERATIONS = 100_000


def binary_search(func, lower=0, upper=None):
    """
    Returns the smallest possible value x such that func(x) is True.

    Args:
    ----
        func (function): The function to be evaluated. It should take a single
            argument and return a boolean value.
        lower (int, optional): The lower bound of the search range. Defaults
            to 0.
        upper (int, optional): The upper bound of the search range. If not
            provided, a reasonable estimate is found based on the initial
            value of lower.

    Returns:
    -------
        int: The smallest value x for which func(x) returns True.

    Raises:
    ------
        BinarySearchError: If upper is provided and func(lower) is equal to
        func(upper).

    Example Usage:
        # Example 1: Finding the smallest positive integer for which the
        # function returns True
        def is_positive(n):
            return n > 0

        result = binary_search(is_positive)
        print(result)  # Output: 1

        # Example 2: Finding the smallest value for which a custom function
        # returns True
        def custom_func(x):
            # Custom logic to determine if x satisfies a condition
            return ...

        result = binary_search(custom_func, lower=10, upper=100)
        print(result)  # Output: Smallest value that satisfies the condition
        # within the range [10, 100]
    """
    lower_bool = func(lower)

    if upper is None:
        iterations = 0
        offset = 1
        while func(lower + offset) == lower_bool:
            offset *= 2
            iterations += 1
            if iterations >= _MAX_UPPER_FIND_ITERATIONS:
                msg = "Cannot find suitable upper bound"
                raise BinarySearchError(msg)
        upper = lower + offset

    else:
        if func(upper) == lower_bool:
            msg = "Supplied function gives the same response for the upper and lower bounds, cannot run binary search"
            raise BinarySearchError(
                msg,
            )

    logger.debug(f"Binary Search Lower: {lower}, Upper: {upper}")

    best_so_far = lower if lower_bool else upper

    while lower <= upper:
        mid = (lower + upper) // 2
        result = func(mid)

        logger.debug(f"Binary search test: {mid} -> {result}")

        if result:
            best_so_far = mid

        if result == lower_bool:
            lower = mid + 1
        else:
            upper = mid - 1

    logger.debug(f"Binary search result: {best_so_far}")

    return best_so_far
