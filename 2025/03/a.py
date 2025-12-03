def run(input: str) -> int:
    total = 0
    for line in input.splitlines():
        left = max(line[:-1])
        left_pos = line.index(left)
        right = max(line[left_pos + 1 :])
        total += int(f"{left}{right}")
    return total
