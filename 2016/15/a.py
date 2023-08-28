import os
import re

from chinese_remainder import chinese_remainder


class Disc:
    def __init__(self, num, size, pos) -> None:
        self.size = size
        self.number = num
        self.position = pos


def run(inputs):
    reg = re.compile(r"\#(\d+).+?(\d+) positions.+?position (\d+)\.$")
    discs = []
    for line in inputs.split(os.linesep):
        matches = map(int, reg.findall(line)[0])
        discs.append(Disc(*matches))
    return chinese_remainder(
        [-d.position - d.number for d in discs],
        [d.size for d in discs],
    )
