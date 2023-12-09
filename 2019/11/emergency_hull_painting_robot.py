from collections import defaultdict
from enum import Enum

import intcode
import numpy as np


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Color(Enum):
    BLACK = 0
    WHITE = 1


class Rotation(Enum):
    ANTICLOCKWISE = 0
    CLOCKWISE = 1


class EhpRobot:
    def __init__(self, intcode_inputs, start_color=Color.BLACK) -> None:
        self.start_color = start_color
        self._direction = Direction.NORTH
        self._position = np.array((0, 0))
        self._path = [self._position.copy()]
        self._colors = defaultdict(lambda: Color.BLACK)
        self._colors[str(self._position)] = self.start_color
        self.program = intcode.optprog(intcode_inputs)

    def run(self):
        while True:
            current_color = self._get_position_color()
            self.program.analyse_intcode(current_color.value)

            if self.program.complete:
                break

            color_cmd = Color(self.program.outputs[-2])
            rotate_cmd = Rotation(self.program.outputs[-1])

            self._set_color(color_cmd)
            self._rotate(rotate_cmd)
            self._step_forward()

    def _step_forward(self):
        delta = {
            Direction.NORTH: [0, +1],
            Direction.EAST: [+1, 0],
            Direction.SOUTH: [0, -1],
            Direction.WEST: [-1, 0],
        }[self._direction]
        self._position += np.array(delta)
        self._path.append(self._position.copy())

    def _rotate(self, rotation):
        if rotation == Rotation.ANTICLOCKWISE:
            delta = -1
        elif rotation == Rotation.CLOCKWISE:
            delta = +1
        else:
            raise NotImplementedError

        self._direction = Direction((self._direction.value + delta + 4) % 4)

    def _set_color(self, color, pos=None):
        if pos is None:
            pos = self._position
        self._colors[str(pos)] = color

    def _get_position_color(self, pos=None):
        if pos is None:
            pos = self._position
        return self._colors[str(pos)]
