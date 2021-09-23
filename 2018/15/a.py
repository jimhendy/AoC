import grid
import units

import exceptions


def run(inputs):

    g = grid.Grid(inputs)
    g.print_grid()

    while True:
        try:
            g.do_round()
            g.print_grid()
        except exceptions.GameOverException:
            break
    g.print_grid()

    print(f"Rounds: {g.rounds}")

    return g.rounds * sum([u.hit_points for u in g.units])
