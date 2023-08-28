import os
from queue import LifoQueue


def run(inputs):
    open_to_close = {"(": ")", "[": "]", "{": "}", "<": ">"}
    opens = set(open_to_close.keys())
    closes = set(open_to_close.values())
    points = {")": 3, "]": 57, "}": 1197, ">": 25137}

    total_syntax_error = 0

    for line in inputs.split(os.linesep):
        lifo = LifoQueue()

        for char in line:
            if char in opens:
                lifo.put(char)
            elif char in closes:
                if char != open_to_close[lifo.get()]:
                    total_syntax_error += points[char]
                    break
            else:
                msg = f'Unknown character "{char}"'
                raise NotImplementedError(msg)

    return total_syntax_error
