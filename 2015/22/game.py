import character


class GameLost(Exception):
    pass


class GameWon(Exception):
    pass


class Game:

    def __init__(self, player_hp, boss_hp, player_mana, boss_damage, hard_mode=False):
        self.player = character.Character(player_hp, player_mana)
        self.boss = character.Character(boss_hp)
        self.boss_damage = boss_damage
        self.game_won = False
        self.turns_complete = 0
        self.hard_mode = hard_mode
        self.spells_used = []

    def copy(self):
        new = Game(
            player_hp=0,
            boss_hp=0,
            player_mana=0,
            boss_damage=self.boss_damage,
            hard_mode=self.hard_mode
        )
        new.player = self.player.copy()
        new.boss = self.boss.copy()
        new.game_won = self.game_won
        new.turns_complete = self.turns_complete
        new.spells_used = [s for s in self.spells_used]
        return new

    def play_turn(self, spell_type):
        """
        Play a single turn for the player and one for the boss
        """
        if self.hard_mode:
            self.player.hp -= 1
            self.check_result()

        self.enact_effects()
        self.check_result()

        self.player.cast_spell(spell_type)
        self.spells_used.append(spell_type.__name__)
        self.enact_effects()
        self.check_result()

        self.player.defend(self.boss_damage)
        self.check_result()

        self.turns_complete += 1

    def check_result(self):
        if self.boss.hp <= 0:
            self.game_won = True
            raise GameWon
        if self.player.hp <= 0:
            raise GameLost

    def enact_effects(self):
        [
            s(self.player, self.boss)
            for s in self.player.active_spells
        ]
        self.player.remove_finished_spells()

    def __lt__(self, other):
        return self.player.used_mana < other.player.used_mana

    def __gt__(self, other):
        return not self.__lt__(other)
