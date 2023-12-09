import os
from enum import Enum, IntEnum

import intcode
import numpy as np


class Direction(IntEnum):
    NORTH = 1
    WEST = 3
    SOUTH = 2
    EAST = 4


class Response(IntEnum):
    WALL = 0
    SUCCESS = 1
    TANK = 2


class MapSymbol(Enum):
    DROID = "D"
    UNKNOWN = " "
    PREVIOUS = "."
    WALL = "#"
    TANK = "@"
    OXYGEN = "O"


def move(pos, direction):
    step = {
        Direction.NORTH: np.array([0, +1]),
        Direction.SOUTH: np.array([0, -1]),
        Direction.WEST: np.array([-1, 0]),
        Direction.EAST: np.array([+1, 0]),
    }[direction]
    return pos + step


class Droid:
    def __init__(self, inputs) -> None:
        self.position = np.zeros(2)
        self.prog = intcode.Intcode(inputs)
        self.layout = {tuple(self.position): MapSymbol.DROID}
        self.tank_position = None
        self.completed_tiles = []
        self.completed_oxygen_tiles = []
        self.on_tank = False

    def __call__(self, instruction: Direction):
        self.prog.analyse_intcode(instruction.value)
        response = Response(self.prog.outputs[-1])
        intended_position = self._get_intended_position(instruction)
        if response == Response.WALL:
            self.layout[tuple(intended_position)] = MapSymbol.WALL
        elif response == Response.SUCCESS:
            if not self.on_tank:
                self.layout[tuple(self.position)] = MapSymbol.PREVIOUS
            else:
                self.on_tank = False
            self.position = intended_position.copy()
            self.layout[tuple(self.position)] = MapSymbol.DROID
        elif response == Response.TANK:
            print(f"Tank found at :{intended_position}")
            self.tank_position = intended_position.copy()
            self.layout[tuple(intended_position)] = MapSymbol.TANK
            self.position = intended_position.copy()
            self.on_tank = True
        return response

    def _get_intended_position(self, instruction):
        return move(self.position, instruction)

    def get_layout(self):
        pos_dtype = np.int32
        pos = np.full((len(self.layout), 2), np.nan, dtype=pos_dtype)
        content = np.full(len(self.layout), np.nan, dtype="object")

        for i, (k, v) in enumerate(self.layout.items()):
            pos[i][0] = k[0]
            pos[i][1] = k[1]
            content[i] = v
        x_min, y_min = pos.min(axis=0)
        x_max, y_max = pos.max(axis=0)
        x_range, y_range = pos.ptp(axis=0) + 1

        expected_values = x_range * y_range
        missing_values = expected_values - len(self.layout)
        if missing_values > 0:
            extra_pos = np.full((missing_values, 2), np.nan, dtype=pos_dtype)
            extra_content = np.full(missing_values, MapSymbol.UNKNOWN, dtype="object")

            count = 0
            for x in range(x_min, x_max + 1):
                for y in range(y_min, y_max + 1):
                    if (x, y) in self.layout:
                        continue
                    extra_pos[count][0] = x
                    extra_pos[count][1] = y
                    count += 1
            pos = np.vstack([pos, extra_pos])
            content = np.hstack([content, extra_content])
        return pos, content

    def plot(self, clear=False):
        pos, content = self.get_layout()

        x_min, y_min = pos.min(axis=0)
        x_max, y_max = pos.max(axis=0)

        if clear:
            os.system("clear")

        for y in range(y_max, y_min - 1, -1):
            for x in range(x_min, x_max + 1):
                c = content[np.all(pos == (x, y), axis=1)][-1]
                print(c.value, end="")
            print()

    def go_to(droid, layout, destination):
        route = droid_route(droid, destination, layout)

        if route is False:
            msg = f"Cannot find route from {droid.position} to {destination}"
            raise Exception(msg)

        for r in route[1:]:
            if r[0] > droid.position[0]:
                yield Direction.EAST
            elif r[0] < droid.position[0]:
                yield Direction.WEST
            elif r[1] > droid.position[1]:
                yield Direction.NORTH
            elif r[1] < droid.position[1]:
                yield Direction.SOUTH
            else:
                raise NotImplementedError

    def find_oxygen_adjacent_cells(self, layout=None):
        if layout is None:
            layout = self.get_layout()
        pos, content = layout
        path_mask = content == MapSymbol.OXYGEN
        path = pos[path_mask]
        pos[:, 0]
        pos[:, 1]

        return_cells = []

        for p in path:
            if tuple(p) in self.completed_oxygen_tiles:
                continue

            for step in [
                Direction.NORTH,
                Direction.EAST,
                Direction.WEST,
                Direction.SOUTH,
            ]:
                new_pos = move(p, step)
                point_index = Droid.array_match_mask(pos, new_pos)
                if any(point_index):
                    c = content[point_index][0]
                    if (c != MapSymbol.WALL) and (c != MapSymbol.OXYGEN):
                        return_cells.append(new_pos)
                    else:
                        continue
            self.completed_oxygen_tiles.append(tuple(p))
        return return_cells

    def find_unknown_cell(self, layout=None):
        if layout is None:
            layout = self.get_layout()
        pos, content = layout
        path_mask = (content == MapSymbol.PREVIOUS) | (content == MapSymbol.DROID)
        path = pos[path_mask]
        pos[:, 0]
        pos[:, 1]
        for p in path[::-1]:
            if tuple(p) in self.completed_tiles:
                continue
            for step in [
                Direction.NORTH,
                Direction.EAST,
                Direction.WEST,
                Direction.SOUTH,
            ]:
                new_pos = move(p, step)
                point_index = Droid.array_match_mask(pos, new_pos)
                if any(point_index):
                    if all(content[point_index] == MapSymbol.UNKNOWN):
                        return new_pos
                    else:
                        continue
                else:
                    return new_pos
            self.completed_tiles.append(tuple(p))
        return False

    @staticmethod
    def random_direction():
        dir_int = np.random.randint(1, 5)
        return Direction(dir_int)

    @staticmethod
    def arrays_match(a, b):
        return np.all(a == b)

    @staticmethod
    def array_match_mask(possibles, arr):
        return np.all(possibles == arr, axis=1)

    @staticmethod
    def remove_array(possibles, arr):
        return possibles[~Droid.array_match_mask(possibles, arr)]

    @staticmethod
    def remove_nan_rows(arr):
        return arr[~np.isnan(arr.sum(axis=1))]

    @staticmethod
    def find_route(origin, destination, possibles):
        route = np.full(possibles.shape, np.nan)
        route[0] = origin.copy()

        remaining_poss = possibles.copy()
        current_pos = origin.copy()
        current_route_it = 1

        while True:
            # If done, return
            if Droid.arrays_match(route[current_route_it - 1], destination):
                return Droid.remove_nan_rows(route)

            # Ensure we can't step back where we came from
            remaining_poss = Droid.remove_array(remaining_poss, current_pos)

            # Possible next steps are next to current position
            poss = remaining_poss[np.abs(remaining_poss - current_pos).sum(axis=1) == 1]

            if not len(poss):
                # No possible steps
                return False
            if len(poss) == 1:
                # Single option
                new_pos = poss[0].copy()
                route[current_route_it] = new_pos
                current_route_it += 1
                current_pos = new_pos
            else:
                # Multiple options

                # Sort the steps so we first go to the one which is closer
                # in Manhatten distance to the destination
                poss = sorted(poss, key=lambda x: np.abs(x - destination).sum())
                poss_next = remaining_poss.copy()
                for p in poss:
                    it_route = Droid.find_route(p, destination, poss_next)
                    if it_route is False:
                        continue
                    route[
                        current_route_it : current_route_it + len(it_route)
                    ] = it_route
                    return Droid.remove_nan_rows(route)
                return False
        return None

    def droid_route(self, destination, layout=None):
        if layout is None:
            layout = self.get_layout()

        pos, content = layout

        mask = (content == MapSymbol.DROID) | (content == MapSymbol.PREVIOUS)
        possible_pos = pos[mask]

        if not any(np.all(possible_pos == destination, axis=1)):
            possible_pos = np.vstack([possible_pos, destination])

        return Droid.find_route(self.position, destination, possible_pos)

    def go_to(self, destination, layout=None):
        if layout is None:
            layout = self.get_layout()

        route = self.droid_route(destination, layout)

        if route is False:
            msg = f"Cannot find route from {self.position} to {destination}"
            raise Exception(msg)

        for r in route[1:]:
            if r[0] > self.position[0]:
                direction = Direction.EAST
            elif r[0] < self.position[0]:
                direction = Direction.WEST
            elif r[1] > self.position[1]:
                direction = Direction.NORTH
            elif r[1] < self.position[1]:
                direction = Direction.SOUTH
            else:
                raise NotImplementedError
            self.__call__(direction)
