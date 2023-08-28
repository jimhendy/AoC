from collections import deque


class Game:
    def __init__(self, last_marble, n_players) -> None:
        self.marbles = deque([0])
        self.next_marble = 1
        self.turn = -1
        self.last_marble = last_marble
        self.n_players = n_players

    def current_player(self):
        return "-" if self.turn == -1 else (self.turn % self.n_players) + 1

    def complete(self):
        return self.next_marble > self.last_marble

    def clockwise(self, n=1):
        self.marbles.rotate(-n)

    def anticlockwise(self, n=1):
        self.marbles.rotate(n)

    def place_new_marble(self):
        marble_number = self.next_marble
        self.next_marble += 1
        self.turn += 1
        if marble_number % 23 == 0:
            return marble_number + self.scoring_turn()
        else:
            self.clockwise(1)
            self.marbles.append(marble_number)
            return 0

    def scoring_turn(self):
        self.anticlockwise(7)
        score = self.marbles.pop()
        self.clockwise(1)
        return score


class Player:
    def __init__(self) -> None:
        self.score = 0
