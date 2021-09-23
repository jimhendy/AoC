import os
import re


def morph(state, grammar):
    new_state = set()
    min_loc = min(state)
    max_loc = max(state)
    for i in range(min_loc - 2, max_loc + 2):
        current = "".join(["#" if i in state else "." for i in range(i - 2, i + 3)])
        try:
            new_pot = grammar[current]
            if new_pot == ".":
                continue
            new_state.add(i)
        except KeyError:
            pass
    return new_state


def run(inputs):

    initial_state = inputs.split(os.linesep)[0].split(":")[1].strip()
    grammar = {
        i.split("=>")[0].strip(): i.split("=>")[1].strip()
        for i in inputs.split(os.linesep)[2:]
    }

    state = set([i for i, c in enumerate(initial_state) if c == "#"])

    data = []

    for _ in range(10_000):
        state = morph(state, grammar)
        data.append(sum(state))
        if _ > 2_000:
            break

    # import matplotlib.pylab as plt
    # plt.plot(data)
    # plt.show()

    # Looks pretty linear from the above

    y1 = data[-1]
    y0 = data[-2]
    x1 = len(data)
    x0 = x1 - 1

    m = (y1 - y0) / (x1 - x0)
    x = int(50e9)
    y = (x - x0) * m + y0

    return y
