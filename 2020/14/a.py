import os
import re


def run(inputs):
    mask = None
    memory = {}
    reg = re.compile(r"mem\[(\d+)\] = (\d+)")
    for line in inputs.split(os.linesep):
        if not len(line.strip()):
            continue

        if line.startswith("mask"):
            mask = line.split("=")[1].strip()
        else:
            register, num = reg.findall(line)[0]
            b_num = f"{int(num):036b}"
            masked_num = int(
                "".join(
                    [n if m == "X" else m for m, n in zip(mask, b_num, strict=False)]
                ),
                2,
            )
            memory[register] = masked_num

    return sum(list(memory.values()))
