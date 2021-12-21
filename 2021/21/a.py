import os


class Die:
    def __init__(self):
        self.rolls = 0

    def roll(self) -> int:
        self.rolls += 1
        r = self.rolls
        while r > 100:
            r -= 100
        return r


class Player:
    def __init__(self, initial_position: int, die: Die):
        self.position = initial_position
        self.die = die
        self.score = 0

    def take_turn(self):
        for _ in range(3):
            self.position += self.die.roll()
            self.position = self.position % 10 or 1
        self.score += self.position


def run(inputs):
    pos = map(int, [line.split()[-1] for line in inputs.split(os.linesep)])

    die = Die()
    players = [Player(initial_position=p, die=die) for p in pos]

    while True:
        for p in players:
            p.take_turn()
            if p.score > 1_000:
                losing_player = [i for i in players if i != p][0]
                return losing_player.score * die.rolls
