class Group:
    def __init__(
        self,
        n_units,
        hit_points,
        attack_damage,
        attack_type,
        initiative,
        weaknesses=None,
        immunities=None,
    ):
        self.n_units = n_units
        self.hit_points = hit_points
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = [] if weaknesses is None else weaknesses
        self.immunities = [] if immunities is None else immunities
        self.target = None

    def copy(self):
        return Group(
            self.n_units,
            self.hit_points,
            self.attack_damage,
            self.attack_type,
            self.initiative,
            self.weaknesses,
            self.immunities,
        )

    def boost(self, b):
        g = self.copy()
        g.attack_damage += b
        return g

    def effective_power(self):
        return self.n_units * self.attack_damage

    def __lt__(self, other):
        ep_diff = self.effective_power() - other.effective_power()
        if not ep_diff:
            return self.initiative < other.initiative
        return ep_diff < 0

    def __gt__(self, other):
        return not self.__lt__(other)

    def calculate_inflicted_damage(self, target):
        if self.attack_type in target.immunities:
            return 0
        damage = self.effective_power()
        if self.attack_type in target.weaknesses:
            damage *= 2
        return damage

    def target_selection(self, available_target_groups):
        target_props = {
            "damage": 0,
            "effective_power": 0,
            "initiative": 0,
            "group": None,
        }
        for t in available_target_groups:
            damage = self.calculate_inflicted_damage(t)
            if damage == 0:
                continue
            replace = (damage > target_props["damage"]) or (
                (damage == target_props["damage"])
                and (
                    (t.effective_power() > target_props["effective_power"])
                    or (
                        (t.effective_power() == target_props["effective_power"])
                        and (t.initiative > target_props["initiative"])
                    )
                )
            )
            if replace:
                target_props["damage"] = damage
                target_props["effective_power"] = t.effective_power()
                target_props["initiative"] = t.initiative
                target_props["group"] = t
        self.target = target_props["group"]
        return self.target

    def __repr__(self):
        return f"{self.n_units} Units"

    def attack(self):
        if self.target is None:
            # print('No target available')
            return
        damage = self.calculate_inflicted_damage(self.target)
        # print(f'{self} attacking {self.target} with damage {damage}')
        units_lost = damage // self.target.hit_points
        if self.target.n_units < units_lost:
            units_lost = self.target.n_units
        self.target.n_units -= units_lost
