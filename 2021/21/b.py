import os
from collections import defaultdict

# Status info: (turns, score, position) : universes

THREE_ROLLS = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}  # roll: weight
TURNS = 0
SCORE = 1
POSITION = 2

class Player:
    def __init__(self, initial_position):
        self.statuses = {(0, 0, initial_position): 1}
        self.turns_to_win = defaultdict(int)
        self.turns_to_not_yet_won = defaultdict(int)

    def _remove_complete(self):
        to_remove = []
        for k, v in self.statuses.items():
            if k[SCORE] >= 21:
                self.turns_to_win[k[TURNS]] += v
                to_remove.append(k)
            else:
                self.turns_to_not_yet_won[k[TURNS]] += v
        for k in to_remove:
            del self.statuses[k]

    def analyse(self):
        while self.statuses:
            new_statuses = defaultdict(int)
            for k, v in self.statuses.items():
                for roll, weight in THREE_ROLLS.items():
                    new_position = (k[POSITION] + roll)
                    while new_position > 10:
                        new_position -= 10
                    new_status = (k[TURNS] + 1, k[SCORE] + new_position, new_position)
                    new_statuses[new_status] += weight * v
            self.statuses = new_statuses
            self._remove_complete()

def run(inputs):
    pos = list(map(int, [line.split()[-1] for line in inputs.split(os.linesep)]))

    p1 = Player(initial_position=pos[0])
    p2 = Player(initial_position=pos[1])

    p1.analyse()
    p2.analyse()

    total_1 = 0
    for r1, w1 in p1.turns_to_win.items():
        nyw2 = p2.turns_to_not_yet_won[r1-1]
        total_1 += w1 * nyw2
    
    total_2 = 0
    for r2, w2 in p2.turns_to_win.items():
        nyw1 = p1.turns_to_not_yet_won[r2]
        total_2 += w2 * nyw1

    return max(total_1, total_2)