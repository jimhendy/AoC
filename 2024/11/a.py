from itertools import chain


def apply_rules(number: int) -> list[int]:
    if number == 0:
        return [1]
    str_number = str(number)
    if (num_digits := len(str_number)) % 2 == 0:
        return [int(str_number[: num_digits // 2]), int(str_number[num_digits // 2 :])]
    return [2024 * number]


def run(inputs: str) -> None:
    numbers = list(map(int, inputs.split()))
    for _ in range(25):
        numbers = chain.from_iterable(apply_rules(num) for num in numbers)

    return sum(1 for _ in numbers)
