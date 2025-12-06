class Point:
    def __init__(self, *x) -> None:
        self.x = x

    def distance(self, other):
        return sum([abs(i - j) for i, j in zip(self.x, other.x, strict=False)])

    def __repr__(self) -> str:
        return ",".join(map(str, self.x))


class Constellation:
    def __init__(self, points) -> None:
        self.points = points

    def distance(self, other):
        return min([i.distance(j) for i in self.points for j in other.points])

    def combine(self, other):
        self.points.extend(other.points)

    def __repr__(self) -> str:
        return "-".join([p.__repr__() for p in self.points])
