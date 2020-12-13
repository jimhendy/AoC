class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def tup(self):
        return (self.x, self.y)

    def __abs__(self):
        return abs(self.x) + abs(self.y)

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        x_diff = self.x - other.x
        if not x_diff:
            return self.y < other.y
        return x_diff < 0

    def __gt__(self, other):
        return not self < other

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return Point(self.x, self.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __hash__(self):
        return hash(f"point_class_hash_{self.x}_{self.y}")

    def nb4(self):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if (dx and dy) or (not dx and not dy):
                    continue
                yield Point(self.x + dx, self.y + dy)

    def nb8(self):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not dx and not dy:
                    continue
                yield Point(self.x + dx, self.y + dy)


    def neighbour(self, direction):
        return self + NEIGHBOUR_DELTAS[direction]


        
NEIGHBOUR_DELTAS = {
    'down': Point(0, 1),
    'up': Point(0, -1),
    'left': Point(-1,0),
    'right': Point(1,0),
    'up-left': Point(-1, -1),
    'up-right': Point(1,-1),
    'down-left': Point(-1,1),
    'down-right': Point(1,1)
}