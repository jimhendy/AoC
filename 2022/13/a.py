from ast import literal_eval


def compare(left, right) -> int:
    """If ordered return True, else return False."""
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        if left == right:
            return 0
        return -1
    if isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    if isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    if isinstance(left, list) and isinstance(right, list):
        for index in range(max(len(left), len(right))):
            if index >= len(left):
                return 1
            if index >= len(right):
                return -1
            c = compare(left[index], right[index])
            if abs(c) == 1:
                return c
        return 0
    return None


def run(inputs):
    sum_of_correct_indicies = 0
    for index, two_lines in enumerate(inputs.split("\n\n"), start=1):
        packet_1, packet_2 = map(literal_eval, two_lines.split())
        if compare(packet_1, packet_2) == 1:
            sum_of_correct_indicies += index
    return sum_of_correct_indicies
