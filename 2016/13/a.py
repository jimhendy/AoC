import a_star

DEST = [31, 39]


class Position(a_star.State):
    def __init__(self, x, y, fav_num, prev_steps=0):
        self.x = x
        self.y = y
        self.fav_num = fav_num
        self.prev_steps = prev_steps

    def metric(self):
        return abs(self.x - DEST[0]) + abs(self.y - DEST[1])

    def __lt__(self, other):
        self.metric() < other.metric()

    def __gt__(self, other):
        return not self.__lt__(other)

    def is_complete(self):
        return self.x == DEST[0] and self.y == DEST[1]

    def is_valid(self):
        return (self.x >= 0 and self.y >= 0) and not is_wall(
            self.x, self.y, self.fav_num
        )

    def all_possible_next_states(self):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy != 0 and dx != 0:
                    continue
                yield Position(
                    self.x + dx, self.y + dy, self.fav_num, self.prev_steps + 1
                )


def run(inputs):
    fav_num = int(inputs)
    n = 10
    for y in range(n):
        for x in range(n):
            if y == 39 and x == 31:
                char = "X"
            elif is_wall(x, y, fav_num):
                char = "#"
            else:
                char = " "
            print(char, end="")
        print()

    initial_state = Position(1, 1, fav_num)
    result = a_star.a_star(initial_state, lambda x: f"{x.x}_{x.y}")
    return result.prev_steps


def is_wall(x, y, favourite_number):
    base_ten = x * x + 3 * x + 2 * x * y + y + y * y + favourite_number
    binary = f"{base_ten:b}"
    return (binary.count("1") % 2) == 1
