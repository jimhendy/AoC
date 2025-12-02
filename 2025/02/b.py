def is_repeated_digits(n: int) -> bool:
    digits = str(n)
    len_ = len(digits)
    for i in range(1, len_ // 2 + 1):
        if digits[:i] * (len_ // i) == digits:
            return True
    return False


def run(input: str) -> int:
    total =0
    for range_ in input.split(","):
        start, end = map(int, range_.split("-"))
        for n in range(start, end + 1):
            if is_repeated_digits(n):
                total += n
    return total