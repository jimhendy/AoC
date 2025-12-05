from dataclasses import dataclass

@dataclass
class Range:
    start: int
    end: int

    def can_combine(self, other: "Range") -> bool:
        return not (self.end < other.start - 1 or other.end < self.start - 1)


def run(input: str) -> int:
    ranges_, _ = input.strip().split("\n\n")
    ranges = []
    for line in ranges_.splitlines():
        start, end = map(int, line.split("-"))
        ranges.append(Range(start, end))

    change = True
    while change:
        change = False
        new_ranges = []
        used = [False] * len(ranges)

        for i, current in enumerate(ranges):
            if used[i]:
                continue
            for j, other in enumerate(ranges[i + 1:], start=i + 1):
                if used[j]:
                    continue
                if current.can_combine(other):
                    current = Range(start=min(current.start, other.start), end=max(current.end, other.end))
                    used[j] = True
                    change = True
            new_ranges.append(current)
            used[i] = True

        ranges = new_ranges

    total = 0
    for r in ranges:
        total += r.end - r.start + 1
    return total
