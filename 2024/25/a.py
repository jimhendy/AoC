class Key:
    def __init__(self, lines: list[str]) -> None:
        self.nums = [len(lines) - 2] * len(lines[0])
        for line in lines[1:-1]:
            for i, char in enumerate(line):
                if char == ".":
                    self.nums[i] -= 1


class Lock:
    def __init__(self, lines: list[str]) -> None:
        self.nums = [0] * len(lines[0])
        for line in lines[1:-1]:
            for i, char in enumerate(line):
                if char == "#":
                    self.nums[i] += 1


def run(inputs: str) -> int:
    locks = []
    keys = []

    for group in inputs.split("\n\n"):
        lines = group.splitlines()

        if lines[0][0] == "#":
            locks.append(Lock(lines))
        else:
            keys.append(Key(lines))

    total = 0

    for key in keys:
        for lock in locks:
            if all(k + l <= 5 for k, l in zip(key.nums, lock.nums, strict=False)):
                total += 1

    return total
