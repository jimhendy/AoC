import os
from typing import List, Union
from collections import deque


class Cuboid:
    def __init__(self, min_x, min_y, min_z, max_x, max_y, max_z):
        self.min_x, self.min_y, self.min_z = min_x, min_y, min_z
        self.max_x, self.max_y, self.max_z = max_x, max_y, max_z
        assert self.max_x >= self.min_x
        assert self.max_y >= self.min_y
        assert self.max_z >= self.min_z

    @classmethod
    def from_init_str(self, init_str: str) -> "Cuboid":
        split = init_str.split()[1].split(",")
        min_x, max_x = list(map(int, split[0][2:].split("..")))
        min_y, max_y = list(map(int, split[1][2:].split("..")))
        min_z, max_z = list(map(int, split[2][2:].split("..")))
        return Cuboid(
            min_x=min_x - 0.5,
            min_y=min_y - 0.5,
            min_z=min_z - 0.5,
            max_x=max_x + 0.5,
            max_y=max_y + 0.5,
            max_z=max_z + 0.5,
        )

    def volume(self):
        return (
            (self.max_x - self.min_x)
            * (self.max_y - self.min_y)
            * (self.max_z - self.min_z)
        )

    def non_overlapping_cuboids(self, other) -> Union[None, List["Cuboid"]]:
        if self.max_x <= other.min_x or self.min_x >= other.max_x:
            return None
        if self.max_y <= other.min_y or self.min_y >= other.max_y:
            return None
        if self.max_z <= other.min_z or self.min_z >= other.max_z:
            return None
        above = Cuboid(
            min_x=min(other.max_x, self.max_x),
            max_x=self.max_x,
            min_y=self.min_y,
            max_y=self.max_y,
            min_z=self.min_z,
            max_z=self.max_z,
        )
        below = Cuboid(
            min_x=self.min_x,
            max_x=max(other.min_x, self.min_x),
            min_y=self.min_y,
            max_y=self.max_y,
            min_z=self.min_z,
            max_z=self.max_z,
        )
        left = Cuboid(
            min_x=below.max_x,
            max_x=above.min_x,
            min_y=self.min_y,
            max_y=max(other.min_y, self.min_y),
            min_z=self.min_z,
            max_z=self.max_z,
        )
        right = Cuboid(
            min_x=below.max_x,
            max_x=above.min_x,
            min_y=min(other.max_y, self.max_y),
            max_y=self.max_y,
            min_z=self.min_z,
            max_z=self.max_z,
        )
        forward = Cuboid(
            min_x=below.max_x,
            max_x=above.min_x,
            min_y=left.max_y,
            max_y=right.min_y,
            min_z=self.min_z,
            max_z=max(other.min_z, self.min_z),
        )
        backward = Cuboid(
            min_x=below.max_x,
            max_x=above.min_x,
            min_y=left.max_y,
            max_y=right.min_y,
            min_z=min(other.max_z, self.max_z),
            max_z=self.max_z,
        )
        return [c for c in (above, below, left, right, forward, backward) if c.volume()]

    def turn_off(self, other: "Cuboid") -> List["Cuboid"]:
        new_cuboids = self.non_overlapping_cuboids(other)
        if new_cuboids is None:
            return [self]
        else:
            return new_cuboids


def run(inputs):
    cuboids = []
    for line in inputs.split(os.linesep):
        is_on = line.startswith("on ")
        new_cuboid = Cuboid.from_init_str(line)

        if is_on:
            new_cuboid_queue = deque([new_cuboid])
            while new_cuboid_queue:
                skip = False
                next_cuboid = new_cuboid_queue.pop()
                for c in cuboids:
                    overlaps = next_cuboid.non_overlapping_cuboids(c)
                    if overlaps is not None:
                        [new_cuboid_queue.append(o) for o in overlaps]
                        skip = True
                        break
                if skip:
                    continue
                cuboids.append(next_cuboid)
        else:
            off_checked_cuboids = []
            for c in cuboids:
                off_checked_cuboids.extend(c.turn_off(new_cuboid))
            cuboids = off_checked_cuboids

    return sum([c.volume() for c in cuboids])