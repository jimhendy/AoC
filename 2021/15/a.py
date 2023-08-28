import os

import numpy as np

from tools.a_star import State, a_star
from tools.point import Point2D


class Route(State):
    def __init__(self, pos, scan, prev_risk=0) -> None:
        self.current_pos = pos
        self.scan = scan
        self.risk = prev_risk + self.scan[self.current_pos.y, self.current_pos.x]

    def is_complete(self):
        return (
            self.current_pos.x == self.scan.shape[1] - 1
            and self.current_pos.y == self.scan.shape[0] - 1
        )

    def is_valid(self):
        return True

    def __lt__(self, other):
        return self.risk < other.risk

    def all_possible_next_states(self):
        for p in self.current_pos.nb4(grid_size=self.scan.shape):
            yield Route(pos=p, scan=self.scan, prev_risk=self.risk)

    def tag(self):
        return self.current_pos


def run(inputs):
    scan = np.array(list(map(list, inputs.split(os.linesep)))).astype(int)

    initial = Route(pos=Point2D(0, 0), scan=scan)
    initial.risk = 0

    best_route = a_star(
        initial_state=initial,
        tag_func=lambda x: x.tag(),
    )

    return best_route.risk
