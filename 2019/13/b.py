import common
import numpy as np
from intcode import optprog


def run(inputs):
    prog = optprog(inputs)
    prog.code[0] = 2

    joystick = 0
    while True:
        prog.analyse_intcode(joystick)

        output = np.array(prog.outputs).reshape(-1, 3)

        score_mask = (output[:, 0] == -1) & (output[:, 1] == 0)
        score = output[score_mask][-1][2]
        tiles = output[~score_mask]

        common.print_game(tiles)

        ball = tiles[tiles[:, 2] == common.Tile.BALL.value][-1]
        paddle = tiles[tiles[:, 2] == common.Tile.PADDLE.value][-1]

        ball_x = ball[0]
        paddle_x = paddle[0]

        joystick = np.sign(ball_x - paddle_x)

        if prog.complete:
            break
        pass

    return score
