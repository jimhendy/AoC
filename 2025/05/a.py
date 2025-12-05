def run(input: str) -> int:
    ranges, ids = input.strip().split("\n\n")
    ranges = [list(map(int, line.split("-"))) for line in ranges.splitlines()]
    ids = list(map(int, ids.splitlines()))

    total = 0
    for id in ids:
        for r in ranges:
            if r[0] <= id <= r[1]:
                total += 1
                break
    return total