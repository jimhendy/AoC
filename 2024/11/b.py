from collections import defaultdict

STEPS = 75


def apply_rules(number: int) -> list[int]:
    if number == 0:
        return [1]
    str_number = str(number)
    if (num_digits := len(str_number)) % 2 == 0:
        return [int(str_number[: num_digits // 2]), int(str_number[num_digits // 2 :])]
    return [2024 * number]


def run(inputs: str) -> None:
    numbers = list(map(int, inputs.split()))

    value_to_count = defaultdict(int)

    for number in numbers:
        value_to_count[number] += 1

    for _ in range(STEPS):
        current_counts = value_to_count.copy()
        for number, count in current_counts.items():
            value_to_count[number] -= count
            for new_number in apply_rules(number):
                value_to_count[new_number] += count

    return sum(value_to_count.values())
