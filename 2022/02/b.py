import numpy as np


def run(inputs):
    # R:1, P:2, S:3
    # Bigger number wins if consequtive, else smaller wins

    str_data = np.array(
        [line.split() for line in inputs.splitlines()], dtype=np.dtype("U1")
    )

    they_play = np.vectorize({"A": 1, "B": 2, "C": 3}.get)(str_data[:, 0])
    game_status = np.vectorize({"X": 0, "Y": 1, "Z": 2}.get)(str_data[:, 1])

    win = game_status == 2
    lose = game_status == 0
    draw = game_status == 1

    we_play = they_play[:]  # Default of draw

    winning_map = {i: i % 3 + 1 for i in range(1, 4)}
    losing_map = {v: k for k, v in winning_map.items()}

    we_play = np.where(win, np.vectorize(winning_map.get)(they_play), we_play)
    we_play = np.where(lose, np.vectorize(losing_map.get)(they_play), we_play)

    return we_play.sum() + win.sum() * 6 + draw.sum() * 3
