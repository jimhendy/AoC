import itertools
import math

DIRECTION_STEPS = {"U": +1j, "D": -1j, "L": -1, "R": +1}
ROPE_LEN = 10


def sign(x: int) -> int:
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


def run(inputs):
    rope = {i: 0 for i in range(ROPE_LEN)}
    tail_locs = {0}
    for direction, steps in (line.split() for line in inputs.splitlines()):
        head_step = DIRECTION_STEPS[direction]
        for _ in range(int(steps)):
            rope[0] += head_step
            for head_i in range(ROPE_LEN - 1):
                delta = rope[head_i] - rope[head_i + 1]
                if abs(delta) < 2:
                    # This rope element did not move so neither will downstream elements
                    break
                rope[head_i + 1] += sign(delta.real) + sign(delta.imag) * 1j
            tail_locs.add(rope[ROPE_LEN - 1])
    return len(tail_locs)
