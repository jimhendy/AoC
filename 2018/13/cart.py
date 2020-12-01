import numpy as np

DIRECTIONS = {
    'LEFT': np.array((0, -1)),
    'RIGHT': np.array((0, +1)),
    'DOWN': np.array((+1, 0)),
    'UP': np.array((-1, 0)),
}

class Cart:

    def __init__(self, loc, track):
        self.loc = loc # np.array(row, col)
        self.track = track
        self.direction = self.initial_direction()
        self.seen_intersections_count = 0

    def initial_direction(self):
        return {
            '>': DIRECTIONS['RIGHT'],
            '<': DIRECTIONS['LEFT'],
            '^': DIRECTIONS['UP'],
            'v': DIRECTIONS['DOWN']
        }[self.current_track_char()]

    def current_track_char(self):
        return self.track[tuple(self.loc)].lower()

    def step(self):
        self.loc += self.direction
        track_char = self.current_track_char()
        if track_char == '/':
            self.direction = {
                'UP': DIRECTIONS['RIGHT'],
                'DOWN': DIRECTIONS['LEFT'],
                'LEFT': DIRECTIONS['DOWN'],
                'RIGHT': DIRECTIONS['UP'],
            }[self.dir_to_str()]
        elif track_char == '\\':
            self.direction = {
                'UP': DIRECTIONS['LEFT'],
                'DOWN': DIRECTIONS['RIGHT'],
                'LEFT': DIRECTIONS['UP'],
                'RIGHT': DIRECTIONS['DOWN'],
            }[self.dir_to_str()]
        elif track_char == '+':
            turn = {
                0: 'left',
                1: 'straight',
                2: 'right'
            }[self.seen_intersections_count%3]
            self.direction = self.evaluate_turn(turn)
            self.seen_intersections_count += 1

    def evaluate_turn(self, turn):
        if turn == 'straight':
            return self.direction
        elif turn == 'left':
            return {
                'UP': DIRECTIONS['LEFT'],
                'RIGHT': DIRECTIONS['UP'],
                'DOWN': DIRECTIONS['RIGHT'],
                'LEFT': DIRECTIONS['DOWN']
            }[self.dir_to_str()]
        elif turn == 'right':
            return {
                'UP': DIRECTIONS['RIGHT'],
                'RIGHT': DIRECTIONS['DOWN'],
                'DOWN': DIRECTIONS['LEFT'],
                'LEFT': DIRECTIONS['UP']
            }[self.dir_to_str()]
        else:
            raise NotImplementedError


    def __lt__(self, other):
        if self.loc[0] == other.loc[0]:
            return self.loc[1] < other.loc[1]
        else:
            return self.loc[0] < other.loc[0]

    def __gt__(self, other):
        return not self.__lt__(other)

    def loc_as_str(self):
        return str(self.loc)

    def dir_to_str(self):
        dir_tup = tuple(self.direction)
        return {
            tuple(v): k
            for k,v in DIRECTIONS.items()
        }[dir_tup]
