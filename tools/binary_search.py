DEBUG = False


def binary_search(func, lower=0, upper=None):
    """
    Returns the smallest possible value x such that func(x) is True.

    # Assumed func(lower) = False and we increase lower until func(x) = True
    # Will also work in reverse case where func(lower) = True and return func(x) = False

    Based on the values of func at lower and upper.
    upper can be provided, otherwise a reasonable estimate is found.
    Assert that func(lower) != func(upper) if upper is provided.
    """

    lower_bool = func(lower)

    if upper is None:
        offset = 1
        while func(lower + offset) == lower_bool:
            offset *= 2
        upper = lower + offset
    else:
        assert func(upper) != lower_bool

    if DEBUG:
        print(f"Binary Search Lower: {lower}, Upper: {upper}")

    best_so_far = lower if lower_bool else upper

    while lower <= upper:
        mid = (lower + upper) // 2
        result = func(mid)

        if DEBUG:
            print(f"Binary search test: {mid} -> {result}")

        if result:
            best_so_far = mid

        if result == lower_bool:
            lower = mid + 1
        else:
            upper = mid - 1

    if DEBUG:
        print(f"Binary search result: {best_so_far}")

    return best_so_far
