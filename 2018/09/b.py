import re

from large_marble_game import Game, Player


def run(inputs):
    data = re.findall(r"(\d+) players; last marble is worth (\d+) points", inputs)[0]

    n_players = int(data[0])
    last_marble = int(data[1]) * 100

    game = Game(last_marble, n_players)
    players = {i: Player() for i in range(1, n_players + 1)}

    while not game.complete():
        score = game.place_new_marble()
        players[game.current_player()].score += score

    return max([p.score for p in players.values()])
