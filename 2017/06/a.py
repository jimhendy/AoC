import numpy as np


def run(inputs):
    blocks = np.array(list(map(int, inputs.split())))
    n_banks = len(blocks)
    seen = set([str(blocks)])
    n_steps = 1
    while True:
        max_index = np.argmax(blocks)
        max_blocks = blocks[max_index]
        blocks[max_index] = 0
        for i in range(max_blocks):
            blocks[(max_index + 1 + i) % n_banks] += 1
        state = str(blocks)
        if state in seen:
            return n_steps
        seen.add(state)
        n_steps += 1
