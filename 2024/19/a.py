from functools import cache


@cache
def can_be_made(available: frozenset[str], desired: str) -> bool:
    if desired in available:
        return True

    for split_point in range(1, len(desired)):
        left, right = desired[:split_point], desired[split_point:]
        if can_be_made(available, left) and can_be_made(available, right):
            return True

    return False


def run(inputs: str) -> int:
    available, desired = inputs.split("\n\n")
    available = frozenset([i.strip() for i in available.split(",")])
    desired = desired.splitlines()

    return sum(can_be_made(available, d) for d in desired)
