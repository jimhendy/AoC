import functools
import operator
from ast import literal_eval


def compare(left, right) -> int:
    """If ordered return True, else return False."""
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        elif left == right:
            return 0
        else:
            return -1
    elif isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    elif isinstance(left, list) and isinstance(right, list):
        for index in range(max(len(left), len(right))):
            if index >= len(left):
                return 1
            elif index >= len(right):
                return -1
            c = compare(left[index], right[index])
            if abs(c) == 1:
                return c
        return 0
    return None


def run(inputs):
    packets = [literal_eval(line) for line in inputs.splitlines() if line]

    extra = [[[2]], [[6]]]

    packets.extend(extra)
    sorted_packets = sorted(packets, key=functools.cmp_to_key(compare), reverse=True)

    return functools.reduce(operator.mul, [sorted_packets.index(e) + 1 for e in extra])
