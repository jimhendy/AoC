class Game:
    def __init__(self, last_marble, n_players) -> None:
        self.marbles = [0]
        self.next_marble = 1
        self.current_marble_index = 0
        self.turn = -1
        self.last_marble = last_marble
        self.n_players = n_players

    def current_player(self):
        return "-" if self.turn == -1 else (self.turn % self.n_players) + 1

    def complete(self):
        return self.next_marble > self.last_marble

    def clockwise(self, n=1):
        for _ in range(n):
            self.current_marble_index += 1
            if self.current_marble_index == len(self.marbles):
                self.current_marble_index = 0

    def anticlockwise(self, n=1):
        for _ in range(n):
            self.current_marble_index -= 1
            if self.current_marble_index == -1:
                self.current_marble_index = len(self.marbles) - 1

    def place_new_marble(self):
        marble_number = self.next_marble
        self.next_marble += 1
        self.turn += 1
        if marble_number % 23 == 0:
            return marble_number + self.scoring_turn()
        loc = (self.current_marble_index + 1) % len(self.marbles) + 1
        self.marbles.insert(loc, marble_number)
        self.current_marble_index = loc
        return 0

    def scoring_turn(self):
        self.anticlockwise(7)
        score = self.marbles.pop(self.current_marble_index)
        if self.current_marble_index == len(self.marbles):
            self.current_marble_index = 0
        return score

    def __repr__(self) -> str:
        out = []
        for i, m in enumerate(self.marbles):
            if i == self.current_marble_index:
                out.append(f"({m})")
            else:
                out.append(str(m))
        return f"[{self.current_player()}] " + " ".join(out)


class Player:
    def __init__(self) -> None:
        self.score = 0
