DIRECTION_STEPS = {"U": +1j, "D": -1j, "L": -1, "R": +1}


def run(inputs):
    head = tail = 0
    tail_locs = {0}
    for direction, steps in (line.split() for line in inputs.splitlines()):
        head_step = DIRECTION_STEPS[direction]
        for _ in range(int(steps)):
            head += head_step
            delta = head - tail
            if abs(delta) >= 2:
                if delta.real and delta.imag:
                    tail += (1 if delta.real > 0 else -1) + (
                        1j if delta.imag > 0 else -1j
                    )
                else:
                    tail += head_step
            tail_locs.add(tail)
    return len(tail_locs)
