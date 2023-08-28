import os
import re

import matplotlib.pylab as plt


class Particle:
    reg = re.compile(
        r"position=<([\s\-\d]+),([\s\-\d]+)> velocity=<([\s\-\d]+),([\s\-\d]+)>",
    )

    def __init__(self, data_str) -> None:
        data = list(map(int, Particle.reg.findall(data_str)[0]))
        self.x = data[0]
        self.y = -data[1]
        self.v_x = data[2]
        self.v_y = -data[3]

    def step(self):
        self.x += self.v_x
        self.y += self.v_y

    def reverse(self):
        self.x -= self.v_x
        self.y -= self.v_y


def num_unique_ys(particles):
    return len({p.y for p in particles})


def run(inputs):
    particles = [Particle(i) for i in inputs.split(os.linesep)]
    prev_ys = 9e99
    ys = num_unique_ys(particles)
    while ys <= prev_ys:
        [p.step() for p in particles]
        prev_ys = ys
        ys = num_unique_ys(particles)

    [p.reverse() for p in particles]

    x = [p.x for p in particles]
    y = [p.y for p in particles]

    plt.hist2d(x, y, bins=(range(min(x), max(x) + 1), range(min(y), max(y) + 1)))
