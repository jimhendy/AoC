import itertools
import os
import re


def run(inputs):
    mask, n_x = None, 0
    memory = {}
    reg = re.compile(r"mem\[(\d+)\] = (\d+)")
    for line in inputs.split(os.linesep):
        if line.startswith("mask"):
            mask = line.split("=")[1].strip()
            n_x = mask.count("X")
        else:
            register, num = reg.findall(line)[0]
            b_reg = f"{int(register):036b}"
            masked_reg = "".join(
                [
                    r if m == "0" else ("1" if m == "1" else "{}")
                    for m, r in zip(mask, b_reg)
                ],
            )
            for xs in set(itertools.combinations([1, 0] * n_x, n_x)):
                r = int(masked_reg.format(*xs), 2)
                memory[r] = int(num)

    return sum(list(memory.values()))
