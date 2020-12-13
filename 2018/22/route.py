from enum import Enum

from a_star import State
from cave import Terrain
from point import Point


class Equipment(Enum):
    Torch = 0
    Climbing = 1
    Empty = 2

class Route(State):
    def __init__(self, pos, cave, equipment, time, history=None):
        self.pos = pos
        self.cave = cave
        self.equipment = equipment
        self.time = time
        self.history = history if history is not None else []

    def __lt__(self, other):
        return self.time < other.time

    def is_complete(self):
        return self.pos == self.cave.target and self.equipment == Equipment.Torch

    def is_valid(self):
        if self.pos.x < 0 or self.pos.y < 0:
            return False
        terrain = self.cave.terrain(self.pos)
        if terrain == Terrain.Rocky:
            return self.equipment != Equipment.Empty
        elif terrain == Terrain.Wet:
            return self.equipment != Equipment.Torch
        elif terrain == Terrain.Narrow:
            return self.equipment != Equipment.Climbing
        else:
            raise NotImplementedError

    def all_possible_next_states(self):
        for p in self.pos.nb4():
            yield Route(p, self.cave, self.equipment, self.time + 1, self.history + [(self.pos.x, self.pos.y, self.equipment.value)])
        for e in Equipment:
            yield Route(self.pos, self.cave, e, self.time + 7,self.history + [(self.pos.x, self.pos.y, self.equipment.value)])
