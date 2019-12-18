import re
import os
import numpy as np
import pandas as pd
from enum import IntEnum, Enum


class Direction(IntEnum):
    NORTH = 1
    WEST = 3
    SOUTH = 2
    EAST = 4
    pass


class Response(IntEnum):
    WALL = 0
    SUCCESS = 1
    KEY = 2
    DOOR = 3
    pass


class MapSymbol(Enum):
    DROID = '@'
    UNKNOWN = ' '
    PREVIOUS = '.'
    WALL = '#'
    pass


def move(pos, direction):
    step = {
        Direction.NORTH: np.array([-1, 0]),
        Direction.SOUTH: np.array([+1, 0]),
        Direction.WEST: np.array([0, -1]),
        Direction.EAST: np.array([0, +1])
    }[direction]
    return pos + step


class Droid():

    def __init__(self, inputs):
        self.position = np.zeros(2)
        self.layout = np.array([list(i) for i in inputs.split(os.linesep)])
        self.position = self.get_current_position()
        self.keys = []
        pass

    def get_current_position(self):
        return np.argwhere(self.layout == MapSymbol.DROID.value)[0]

    def __call__(self, instruction: Direction):

        intended_position = self._get_intended_position(instruction)
        at_new_position = self.layout[intended_position[0]][intended_position[1]]
        response = self.new_pos_response(at_new_position)

        if response == Response.SUCCESS:
            self.layout[self.position[0]][self.position[1]] = MapSymbol.PREVIOUS.value
            self.position = intended_position.copy()
            self.layout[self.position[0]][self.position[1]] = MapSymbol.DROID.value
            pass
        elif response == Response.KEY:
            self.keys.append(at_new_position)
            self.layout[self.position[0]][self.position[1]] = MapSymbol.PREVIOUS.value
            self.position = intended_position.copy()
            self.layout[self.position[0]][self.position[1]] = MapSymbol.DROID.value
            pass
        elif response == Response.DOOR:
            required_key = at_new_position.lower()
            if not required_key in self.keys:
                raise Exception(
                    f'Walked into a locked door ({at_new_position})')
            self.layout[self.position[0]][self.position[1]] = MapSymbol.PREVIOUS.value
            self.position = intended_position.copy()
            self.layout[self.position[0]][self.position[1]] = MapSymbol.DROID.value
            pass
        elif response == Response.WALL:
            raise Exception('Walked into a wall')
        else:
            raise NotImplemented
        
        return response

    def new_pos_response(self, at_new_position):
        if at_new_position == MapSymbol.WALL.value:
            response = Response.WALL
        elif at_new_position == MapSymbol.PREVIOUS.value:
            response = Response.SUCCESS
        elif self.is_key(at_new_position):
            response = Response.KEY
        elif self.is_door(at_new_position):
            response = Response.DOOR
        else:
            raise NotImplemented
        return response

    def is_key(self, char):
        return char == char.lower()

    def is_door(self, char):
        return char == char.upper()

    def _get_intended_position(self, instruction):
        return move(self.position, instruction)

    def plot(self, clear=False):
        if clear:
            os.system('clear')
            pass
        [print(j, end='')
         for j in os.linesep.join([''.join(i) for i in self.layout])]
        print()
        pass

    def key_positions(self):
        ascii_ = np.array([[ord(j) for j in i] for i in self.layout])
        key_pos = np.argwhere((ascii_ >= 97) & (ascii_ <= 122))
        key_dict = {self.layout[k[0]][k[1]]: k for k in key_pos}
        return key_dict
    
    def find_accessible_keys(self):
        reg = re.compile('^[a-z\@\.' + ''.join([i.upper() for i in self.keys]) + ']$')
        vmatch = np.vectorize(lambda x:bool(reg.match(x)))
        possibles = np.argwhere(vmatch(self.layout))
        kps = self.key_positions()
        routes = {}
        for key, location in kps.items():
            route = Droid.find_route(self.position, location, possibles)
            if route is False:
                continue
            routes[key] = route
            pass
        if not len(routes):
            return False
        return routes

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
            if Droid.arrays_match(route[current_route_it-1], destination):
                return Droid.remove_nan_rows(route)

            # Ensure we can't step back where we came from
            remaining_poss = Droid.remove_array(remaining_poss, current_pos)

            # Possible next steps are next to current position
            poss = remaining_poss[np.abs(
                remaining_poss-current_pos).sum(axis=1) == 1]

            if not len(poss):
                # No possible steps
                return False
            if len(poss) == 1:
                # Single option
                new_pos = poss[0].copy()
                route[current_route_it] = new_pos
                current_route_it += 1
                current_pos = new_pos
                pass
            else:
                # Multiple options

                # Sort the steps so we first go to the one which is closer
                # in Manhatten distance to the destination
                poss = sorted(poss, key=lambda x: np.abs(x-destination).sum())
                poss_next = remaining_poss.copy()
                for p in poss:
                    it_route = Droid.find_route(p, destination, poss_next)
                    if it_route is False:
                        continue
                    route[current_route_it: current_route_it +
                          len(it_route)] = it_route
                    return Droid.remove_nan_rows(route)
                return False
            pass
        pass

    def go_to(self, destination):
        if all(destination==self.position):
            return 
        if destination[1] > self.position[1]:
            direction = Direction.EAST
        elif destination[1] < self.position[1]:
            direction = Direction.WEST
        elif destination[0] < self.position[0]:
            direction = Direction.NORTH
        elif destination[0] > self.position[0]:
            direction = Direction.SOUTH
        else:
            raise NotImplementedError
        self.__call__(direction)
        pass
