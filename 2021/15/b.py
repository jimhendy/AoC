import os
import numpy as np
import heapq

ID_RO_RISK = {}
MAP_SIZE = None
STEPS = ((-1, 0), (1, 0), (0, 1), (0, -1))


def a_star(initial_state):
    possible_states = [initial_state]
    seen = set()
    while len(possible_states):
        best_option = heapq.heappop(possible_states)
        if best_option.is_complete():
            return best_option
        for s in best_option.all_possible_next_states():
            if s._id in seen:
                continue
            seen.add(s._id)
            heapq.heappush(possible_states, s)


class Route:
    __slots__ = ["x", "y", "_id", "risk"]

    def __init__(self, x, y, prev_risk=0):
        self.x = x
        self.y = y
        self._id = self.x * MAP_SIZE + self.y
        self.risk = prev_risk + ID_RO_RISK[self._id]

    def is_complete(self):
        return self.x == MAP_SIZE - 1 and self.y == MAP_SIZE - 1

    def __lt__(self, other):
        return self.risk < other.risk

    def all_possible_next_states(self):
        for dx, dy in STEPS:
            new_x = self.x + dx
            if not 0 <= new_x < MAP_SIZE:
                continue

            new_y = self.y + dy
            if not 0 <= new_y < MAP_SIZE:
                continue

            yield Route(x=new_x, y=new_y, prev_risk=self.risk)


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
    assert scan.shape[0] == scan.shape[1]
    MAP_SIZE = scan.shape[0]

    for y, row in enumerate(scan):
        for x, risk in enumerate(row):
            ID_RO_RISK[x * MAP_SIZE + y] = risk

    initial = Route(x=0, y=0)
    initial.risk = 0

    best_route = a_star(initial_state=initial)

    return best_route.risk
