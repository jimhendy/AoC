import os
import re

import numpy as np


class Claim:

    reg = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")

    def __init__(self, data):
        self.data = data
        match = Claim.reg.findall(self.data)[0]
        self.num = match[0]
        self.start_x = int(match[1])
        self.start_y = int(match[2])
        self.width = int(match[3])
        self.height = int(match[4])
        self.end_x = self.start_x + self.width
        self.end_y = self.start_y + self.height


def run(inputs):
    claims = [Claim(i) for i in inputs.splitlines()]
    max_x = max([c.end_x for c in claims])
    max_y = max([c.end_y for c in claims])
    fabric = np.zeros((max_x + 1, max_y + 1))
    for c in claims:
        for x in range(c.start_x, c.end_x):
            for y in range(c.start_y, c.end_y):
                fabric[x][y] += 1

    for c in claims:
        overlap = False
        for x in range(c.start_x, c.end_x):
            for y in range(c.start_y, c.end_y):
                if fabric[x][y] != 1:
                    overlap = True
                    break
            if overlap:
                continue
        if not overlap:
            return c.num
