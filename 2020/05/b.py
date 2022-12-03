import os

import numpy as np


def extract_seat_num(seat, num, lower="F", upper="B"):
    possibles = list(range(num))
    i = 0
    while len(possibles) > 1:
        char = seat[i]
        if char == lower:
            possibles = possibles[: len(possibles) // 2]
        elif char == upper:
            possibles = possibles[len(possibles) // 2 :]
        else:
            raise NotImplementedError
        i += 1
    return possibles[0], seat[i:] if i < len(seat) else None


def analyse_ticket(seat, rows=128, cols=8):
    row, col_seat = extract_seat_num(seat, rows)
    col, _ = extract_seat_num(col_seat, cols, "L", "R")
    return row * cols + col


def run(inputs):
    ids = [analyse_ticket(s) for s in inputs.split(os.linesep)]
    missing = [
        i
        for i in range(min(ids), max(ids))
        if i not in ids and (i - 1) in ids and (i + 1) in ids
    ]
    return missing[0]
