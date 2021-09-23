import re
import os
import numpy as np

from collections import defaultdict

NUM = "[ \-\d]+"


class Particle:
    def __init__(self, particle_id, config_str):
        self.particle_id = particle_id
        data = list(
            map(
                int,
                re.findall(
                    f"^p=<({NUM}),({NUM}),({NUM})>, v=<({NUM}),({NUM}),({NUM})>, a=<({NUM}),({NUM}),({NUM})>$",
                    config_str,
                )[0],
            )
        )
        self.position = np.array([data[0], data[1], data[2]])
        self.velocity = np.array([data[3], data[4], data[5]])
        self.acceleration = np.array([data[6], data[7], data[8]])
        pass

    def distance(self):
        return np.sum(np.abs(self.position))

    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity


def run(inputs):
    particles = [Particle(i, l) for i, l in enumerate(inputs.split(os.linesep))]

    for _ in range(1_000):
        [p.update() for p in particles]
        positions = defaultdict(list)
        for p in particles:
            pos = "_".join(list(map(str, p.position)))
            positions[pos].append(p)
        for k, v in positions.items():
            if len(v) > 1:
                for p in v:
                    particles.remove(p)

    return len(particles)
