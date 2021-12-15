import os
import numpy as np
from tools.a_star import State
import heapq

POINT_TO_RISK = {}
MAP_SIZE = None
STEPS = ((-1, 0), (1, 0), (0, 1), (0, -1))


def a_star(initial_state, tag_func=str):
    possible_states = [initial_state]
    seen = set()
    while len(possible_states):
        best_option = heapq.heappop(possible_states)
        if best_option.is_complete():
            return best_option
        for s in best_option.all_possible_next_states():
            tag = tag_func(s)
            if tag in seen:
                continue
            seen.add(tag)
            heapq.heappush(possible_states, s)


class Route(State):
    def __init__(self, pos, prev_risk=0):
        self.current_pos = pos
        self.risk = prev_risk + POINT_TO_RISK[self.current_pos]

    def is_complete(self):
        return (
            self.current_pos[0] == MAP_SIZE - 1 and self.current_pos[1] == MAP_SIZE - 1
        )

    def is_valid(self):
        return True

    def __lt__(self, other):
        return self.risk < other.risk

    def all_possible_next_states(self):
        for dx, dy in STEPS:
            new_x = self.current_pos[0] + dx
            if not 0 <= new_x < MAP_SIZE:
                continue

            new_y = self.current_pos[1] + dy
            if not 0 <= new_y < MAP_SIZE:
                continue

            yield Route(pos=(new_x, new_y), prev_risk=self.risk)

    def tag(self):
        return self.current_pos


def run(inputs):
    global MAP_SIZE
    orig_scan = np.array(list(map(list, inputs.split(os.linesep)))).astype(int)
    scan = np.array(
        [
            [(char + x + y) for x in range(5) for char in row]
            for y in range(5)
            for row in orig_scan
        ]
    )
    scan[scan > 9] += scan[scan > 9] // 10  # > 9 wraps to 1, not 0
    scan = np.mod(scan, 10)
    for y, row in enumerate(scan):
        for x, risk in enumerate(row):
            POINT_TO_RISK[(x, y)] = risk

    assert scan.shape[0] == scan.shape[1]
    MAP_SIZE = scan.shape[0]

    initial = Route(pos=(0, 0))
    initial.risk = 0

    best_route = a_star(
        initial_state=initial,
        tag_func=lambda x: x.tag(),
    )

    return best_route.risk