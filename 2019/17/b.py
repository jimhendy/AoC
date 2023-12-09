import os
from enum import Enum

import intcode
import numpy as np


class MapSymbol(Enum):
    EMPTY = "."
    LADDER = "#"
    DROID_UP = "^"
    DROID_LEFT = "<"
    DROID_RIGHT = ">"
    DROID_DOWN = "v"
    NEWLINE = "\n"


DROID_CHARS = [
    MapSymbol.DROID_UP,
    MapSymbol.DROID_LEFT,
    MapSymbol.DROID_RIGHT,
    MapSymbol.DROID_DOWN,
]


class Turn(Enum):
    RIGHT = "R"
    LEFT = "L"
    NONE = "0"


class Direction(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3


direction_map = {
    MapSymbol.DROID_UP: Direction.UP,
    MapSymbol.DROID_LEFT: Direction.LEFT,
    MapSymbol.DROID_DOWN: Direction.DOWN,
    MapSymbol.DROID_RIGHT: Direction.RIGHT,
}

symbol_map = {v: k for k, v in direction_map.items()}


def left_turn(direction):
    return {
        Direction.UP: Direction.LEFT,
        Direction.LEFT: Direction.DOWN,
        Direction.DOWN: Direction.RIGHT,
        Direction.RIGHT: Direction.UP,
    }[direction]


def right_turn(direction):
    return {
        Direction.UP: Direction.RIGHT,
        Direction.LEFT: Direction.UP,
        Direction.DOWN: Direction.LEFT,
        Direction.RIGHT: Direction.DOWN,
    }[direction]


def get_droid_position(layout):
    pos = np.argwhere(np.isin(layout, DROID_CHARS))
    assert pos.shape[0] == 1
    return pos[0]


def get_droid_symbol(layout):
    pos = get_droid_position(layout)
    return layout[pos[0]][pos[1]]


def get_droid_direction(layout):
    droid = get_droid_symbol(layout)
    return {
        MapSymbol.DROID_UP: Direction.UP,
        MapSymbol.DROID_LEFT: Direction.LEFT,
        MapSymbol.DROID_DOWN: Direction.DOWN,
        MapSymbol.DROID_RIGHT: Direction.RIGHT,
    }[droid]


def get_step(direction):
    return {
        Direction.UP: np.array([-1, 0]),
        Direction.LEFT: np.array([0, -1]),
        Direction.RIGHT: np.array([0, +1]),
        Direction.DOWN: np.array([+1, 0]),
    }[direction]


def space_is_symbol(coords, layout, symbol):
    if any(coords < 0):
        return False
    if any(coords >= layout.shape):
        return False
    return layout[coords[0]][coords[1]] == symbol


def get_turn(layout):
    pos = get_droid_position(layout)
    direction = get_droid_direction(layout)

    step = get_step(direction)
    # If ladder straight ahead then do not turn
    new_pos = pos + step
    if space_is_symbol(new_pos, layout, MapSymbol.LADDER):
        return Turn.NONE

    # Let's try a left turn
    new_direction = left_turn(direction)
    step = get_step(new_direction)
    new_pos = pos + step
    if space_is_symbol(new_pos, layout, MapSymbol.LADDER):
        return Turn.LEFT

    # Let's try a left turn
    new_direction = right_turn(direction)
    step = get_step(new_direction)
    new_pos = pos + step
    if space_is_symbol(new_pos, layout, MapSymbol.LADDER):
        return Turn.RIGHT

    # END
    return False


def run(inputs):
    prog = intcode.Intcode(inputs)
    prog.analyse_intcode()

    data = np.array(list(map(chr, prog.outputs)))[:-1]
    data = data.reshape(-1, int(np.argwhere(data == os.linesep)[0] + 1))

    A = "R,10,L,10,L,12,R,6"
    B = "L,10,R,12,R,12"
    C = "R,6,R,10,L,10"

    MMR = ["B", "C", "B", "A", "C", "A", "C", "A", "B", "A"]

    layout = np.array([[MapSymbol(i) for i in d] for d in data])

    commands = []
    steps = 0
    prev_pos = get_droid_position(layout)
    while True:
        turn = get_turn(layout)
        print(turn)
        direction = get_droid_direction(layout)
        if turn == Turn.LEFT:
            commands.append(str(steps))
            commands.append("L")
            steps = 0
            layout[prev_pos[0]][prev_pos[1]] = symbol_map[left_turn(direction)]
        elif turn == Turn.RIGHT:
            commands.append(str(steps))
            commands.append("R")
            steps = 0
            layout[prev_pos[0]][prev_pos[1]] = symbol_map[right_turn(direction)]
        elif turn == Turn.NONE:
            steps += 1
            step = get_step(direction)
            new_pos = prev_pos + step
            symbol = get_droid_symbol(layout)
            layout[prev_pos[0]][prev_pos[1]] = MapSymbol.LADDER
            layout[new_pos[0]][new_pos[1]] = symbol
            prev_pos = new_pos
        else:
            print(f"Returned : {turn}")
            break

        os.system("clear")
        [print(i.value, end="") for i in layout.ravel()]
    commands.append(steps)
    commands = ",".join(list(map(str, commands[1:])))
    print(commands)

    inputs2 = inputs[:]
    inputs2 = "2" + inputs[1:]
    prog2 = intcode.Intcode(inputs2)

    prog2.analyse_intcode()
    [prog2.analyse_intcode(ord(i)) for i in ",".join(MMR)]
    prog2.analyse_intcode(ord(os.linesep))
    [prog2.analyse_intcode(ord(i)) for i in ",".join(A.split(","))]
    prog2.analyse_intcode(ord(os.linesep))
    [prog2.analyse_intcode(ord(i)) for i in ",".join(B.split(","))]
    prog2.analyse_intcode(ord(os.linesep))
    [prog2.analyse_intcode(ord(i)) for i in ",".join(C.split(","))]
    prog2.analyse_intcode(ord(os.linesep))
    prog2.analyse_intcode(ord("n"))
    prog2.analyse_intcode(ord(os.linesep))

    return prog2.outputs[-1]
