def is_repeated_digits(n: int) -> bool:
    digits = str(n)
    half = len(digits) // 2
    return digits[:half] == digits[half:]


def run(input: str) -> int:
    total =0
    for range_ in input.split(","):
        start, end = map(int, range_.split("-"))
        for n in range(start, end + 1):
            if is_repeated_digits(n):
                total += n
    return total