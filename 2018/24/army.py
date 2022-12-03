import re

from group import Group


class Army:
    def __init__(self, name):
        self.name = name
        self.groups = []
        self.basic_reg = re.compile(
            r"(\d+) units.+?(\d+) hit points.+?(\d+) (\w+) damage.+?(\d+)"
        )
        self.weakness_reg = re.compile(r"weak to ([^;\)]+)")
        self.immunity_reg = re.compile(r"immune to ([^;\)]+)")

    def copy(self):
        a = Army(self.name)
        a.groups = [g.copy() for g in self.groups]
        return a

    def boost(self, b):
        a = Army(self.name)
        a.groups = [g.boost(b) for g in self.groups]
        return a

    def add_group(self, input_line):
        basic = self.basic_reg.findall(input_line)[0]
        weak = self.weakness_reg.findall(input_line)
        immune = self.immunity_reg.findall(input_line)

        new_group = Group(
            n_units=int(basic[0]),
            hit_points=int(basic[1]),
            attack_damage=int(basic[2]),
            attack_type=basic[3],
            initiative=int(basic[4]),
            weaknesses=None
            if not len(weak)
            else [w.strip() for w in weak[0].split(",")],
            immunities=None
            if not len(immune)
            else [i.strip() for i in immune[0].split(",")],
        )
        self.groups.append(new_group)

    def bring_out_your_dead(self):
        to_remove = [i for i, g in enumerate(self.groups) if g.n_units <= 0][::-1]
        [self.groups.pop(i) for i in to_remove]
