import re

import numpy as np


class Moon:
    def __init__(self, pos_str):
        self.pos_str = pos_str
        self.position = self.extract_pos()
        self.velocity = np.array([0, 0, 0])
        pass

    def extract_pos(self):
        pos = np.array([int(i) for i in re.findall("([-\d]+)", self.pos_str)])
        return pos

    def pot_energy(self):
        return np.abs(self.position).sum()

    def kin_energy(self):
        return np.abs(self.velocity).sum()

    def energy(self):
        return self.pot_energy() * self.kin_energy()

    def print_data(self):
        return (
            f"pos=<x= {self.position[0]}, y= {self.position[1]}, z= {self.position[2]}>, "
            + f"vel=<x= {self.velocity[0]}, y= {self.velocity[1]}, z= {self.velocity[2]}>"
        )
        pass

    def update_velocity(self, directions):
        self.velocity = np.add(self.velocity, directions)
        pass

    def update_position(self):
        self.position = np.add(self.position, self.velocity)
        pass

    pass
