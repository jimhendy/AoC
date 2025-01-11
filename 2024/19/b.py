from functools import lru_cache


@lru_cache(maxsize=None)
def possible_combinations(available: frozenset[str], desired: str) -> int:
    count = int(desired in available)

    for split_point in range(1, len(desired)):
        left, right = desired[:split_point], desired[split_point:]
        if left in available:
            count += possible_combinations(available, right)

    return count


def run(inputs: str) -> int:
    available, desired = inputs.split("\n\n")
    available = frozenset([i.strip() for i in available.split(",")])
    desired = desired.splitlines()

    return sum(possible_combinations(available, d) for d in desired)
