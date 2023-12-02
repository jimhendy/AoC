def run(inputs: str) -> int:
    total = 0
    for line in inputs.splitlines():
        first = next(x for x in line if x.isnumeric())
        last = next(x for x in line[::-1] if x.isnumeric())
        total += int(f"{first}{last}")
    return total
