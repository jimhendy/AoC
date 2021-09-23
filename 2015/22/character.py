import game


class Character:
    def __init__(self, hp, mana=0, armor=0):
        self.hp = hp
        self.mana = mana
        self.used_mana = 0
        self.armor = armor
        self.active_spells = []

    def remove_finished_spells(self):
        self.active_spells = [s for s in self.active_spells if s.is_active()]

    def defend(self, attack_damage):
        strength = max([attack_damage - self.armor, 1])
        self.hp -= strength

    def cast_spell(self, spell_type):
        if len(
            [
                s
                for s in self.active_spells
                if isinstance(s, spell_type) and s.is_active()
            ]
        ):
            raise game.GameLost
        spell = spell_type()
        self.mana -= spell.mana_cost
        if self.mana < 0:
            raise game.GameLost
        self.used_mana += spell.mana_cost
        self.active_spells.append(spell)

    def copy(self):
        new = Character(hp=self.hp, mana=self.mana, armor=self.armor)
        new.active_spells = [s.copy() for s in self.active_spells]
        new.used_mana = self.used_mana
        return new
