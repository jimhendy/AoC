import heapq
import re

import game
import spells


def run(inputs):
    available_spells = [
        spells.MagicMissile,
        spells.Drain,
        spells.Shield,
        spells.Poison,
        spells.Recharge,
    ]

    boss_hp = int(re.findall(r"Hit Points: (\d+)", inputs)[0])
    boss_damage = int(re.findall(r"Damage: (\d+)", inputs)[0])

    player_hp = 50
    player_mana = 500

    possible_games = [
        game.Game(player_hp, boss_hp, player_mana, boss_damage, hard_mode=True),
    ]

    while True:
        best_option = heapq.heappop(possible_games)

        if best_option.game_won:
            break

        for s in available_spells:
            gc = best_option.copy()
            try:
                gc.play_turn(s)
            except game.GameLost:
                continue
            except game.GameWon:
                pass
            heapq.heappush(possible_games, gc)

    return best_option.player.used_mana
