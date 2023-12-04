def run(inputs: str) -> int:
    total = 0
    for line in inputs.splitlines():
        winning_numbers, numbers_you_have = line.split(":")[1].split("|")
        intersection = set(map(int, winning_numbers.split())).intersection(
            map(int, numbers_you_have.split()),
        )
        total += bool(intersection) * 2 ** (len(intersection) - 1)

    return total
