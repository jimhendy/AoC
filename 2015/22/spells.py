from abc import ABC


class Spell(ABC):
    def __init__(
        self,
        mana_cost,
        n_turns=1,
        damage=0,
        hp=0,
        armor=0,
        mana=0,
        each_time=False,
    ) -> None:
        self.mana_cost = mana_cost
        self.n_turns = n_turns
        self.remaining_turns = self.n_turns
        self.damage = damage
        self.hp = hp
        self.armor = armor
        self.mana = mana
        self.each_time = each_time

    def __call__(self, player, boss):
        if (self.remaining_turns == self.n_turns) or self.each_time:
            player.hp += self.hp
            player.armor += self.armor
            player.mana += self.mana
            if self.damage > 0:
                boss.defend(self.damage)

        self.remaining_turns -= 1

        if self.remaining_turns == 0:
            player.armor -= self.armor

    def is_active(self):
        return self.remaining_turns > 0

    def copy(self):
        new = self.__class__()
        new.remaining_turns = self.remaining_turns
        return new


class MagicMissile(Spell):
    def __init__(self) -> None:
        super().__init__(53, damage=4)


class Drain(Spell):
    def __init__(self) -> None:
        super().__init__(73, damage=2, hp=2)


class Shield(Spell):
    def __init__(self) -> None:
        super().__init__(113, armor=7, n_turns=6)


class Poison(Spell):
    def __init__(self) -> None:
        super().__init__(173, damage=3, n_turns=6, each_time=True)


class Recharge(Spell):
    def __init__(self) -> None:
        super().__init__(229, mana=101, n_turns=5, each_time=True)
