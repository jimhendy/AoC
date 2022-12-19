import re

REG_NUM = r"(-?\d+)"
REG = re.compile(
    f"^Sensor at x={REG_NUM}, y={REG_NUM}: closest beacon is at x={REG_NUM}, y={REG_NUM}$"
)

Y = 2_000_000


class Range:
    def __init__(self, lower: int, upper: int) -> None:
        self.lower = lower
        self.upper = upper

    def overlaps(self, other: "Range") -> bool:
        left = self if self.lower < other.lower else other
        right = self if other is left else other
        return left.lower <= right.upper and right.lower <= left.upper

    def combine(self, other: "Range") -> "Range":
        return Range(min(self.lower, other.lower), max(self.upper, other.upper))

    def __len__(self) -> int:
        return self.upper - self.lower

    def __repr__(self):
        return f"Range({self.lower},{self.upper})"


def run(inputs):
    ranges = []
    for line in inputs.splitlines():
        sx, sy, bx, by = map(int, REG.findall(line)[0])
        distance = abs(bx - sx) + abs(by - sy)
        dist_to_y = abs(Y - sy)
        width_at_y = distance - dist_to_y
        if width_at_y > 0:
            ranges.append(Range(lower=sx - width_at_y, upper=sx + width_at_y))

    # Remove double counting
    while True:
        combined = False
        for i, ri in enumerate(ranges):
            for j, rj in enumerate(ranges):
                if i == j:
                    continue
                if ri.overlaps(rj):
                    new_range = ri.combine(rj)
                    ranges = [r for k, r in enumerate(ranges) if k not in [i, j]]
                    ranges.append(new_range)
                    combined = True
                    break
            if combined:
                break
        if not combined:
            break

    return sum(len(r) for r in ranges)
