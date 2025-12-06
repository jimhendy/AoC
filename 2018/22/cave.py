import os
from enum import Enum

from point import Point


class Terrain(Enum):
    Rocky = 0
    Wet = 1
    Narrow = 2


CHARACTERS = {Terrain.Rocky: ".", Terrain.Wet: "=", Terrain.Narrow: "|", "unknown": " "}


class Cave:
    def __init__(self, depth, target) -> None:
        self.depth = depth
        self.target = target
        self.erosion_level_cache = {}  # Keyed by point
        self.geologic_index_cache = {}
        self.terrain_cache = {}
        self.grid = []

    def geologic_index(self, p):
        if p in self.geologic_index_cache:
            return self.geologic_index_cache[p]

        if (p.x == 0 and p.y == 0) or p == self.target:
            gi = 0
        elif p.y == 0:
            gi = p.x * 16807
        elif p.x == 0:
            gi = p.y * 48271
        else:
            gi = self.erosion_level(p.neighbour("left")) * self.erosion_level(
                p.neighbour("up"),
            )

        self.geologic_index_cache[p] = gi
        return gi

    def erosion_level(self, p):
        if p in self.erosion_level_cache:
            return self.erosion_level_cache[p]

        gi = self.geologic_index(p)
        return (gi + self.depth) % 20183

    def terrain(self, p):
        if p in self.terrain_cache:
            return self.terrain_cache[p]
        el = self.erosion_level(p)
        terrain = Terrain(el % 3)
        self.terrain_cache[p] = terrain
        return terrain

    def __repr__(self) -> str:
        max_x = max([p.x for p in self.terrain_cache])
        max_y = max([p.y for p in self.terrain_cache])

        out = ""
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                p = Point(x, y)
                if p == self.target:
                    out += "T"
                else:
                    out += CHARACTERS.get(self.terrain_cache.get(p, "unknown"))
            out += os.linesep
        return out
