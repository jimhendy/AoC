import os
from collections import defaultdict


def run(inputs):
    initial_state = inputs.split(os.linesep)[0].split(":")[1].strip()
    grammar = {
        i.split("=>")[0].strip(): i.split("=>")[1].strip()
        for i in inputs.split(os.linesep)[2:]
    }

    state = defaultdict(lambda: ".")
    for i, c in enumerate(list(initial_state)):
        state[i] = c

    print("".join([state[k] for k in sorted(state.keys())]))

    for _ in range(20):
        new_state = defaultdict(lambda: ".")
        for i in range(min(state.keys()) - 2, max(state.keys()) + 2):
            current = "".join([state[i] for i in range(i - 2, i + 3)])
            try:
                new_state[i] = grammar[current]
            except KeyError:
                new_state[i] = "."
        state = new_state
        print("".join([state[k] for k in sorted(state.keys())]))

    return sum([k for k, v in state.items() if v == "#"])
