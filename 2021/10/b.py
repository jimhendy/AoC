import os
from queue import LifoQueue

import numpy as np


def run(inputs):
    open_to_close = {"(": ")", "[": "]", "{": "}", "<": ">"}
    opens = set(open_to_close.keys())
    closes = set(open_to_close.values())
    points = {"(": 1, "[": 2, "{": 3, "<": 4}

    scores = []

    for line in inputs.split(os.linesep):
        lifo = LifoQueue()
        skip_line = False

        for char in line:
            if char in opens:
                lifo.put(char)
            elif char in closes:
                if char != open_to_close[lifo.get()]:
                    skip_line = True
                    break
            else:
                msg = f'Unknown character "{char}"'
                raise NotImplementedError(msg)

        if not skip_line:
            line_score = 0
            while lifo.qsize():
                line_score *= 5
                line_score += points[lifo.get()]
            scores.append(line_score)

    return np.median(scores)
