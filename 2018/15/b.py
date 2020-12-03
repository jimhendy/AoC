import grid
import units

import exceptions

def run(inputs):

    elf_power = 3

    while True:

        print('='*40)
        print(f'Trying Elf Power: {elf_power}')

        g = grid.Grid(inputs, elf_power=elf_power)
        initial_elves = g.unit_counts['E']
        g.print_grid()

        while True:
            try:
                g.do_round()
                if g.unit_counts['E'] != initial_elves:
                    # Dead elf
                    break
                g.print_grid()
            except exceptions.GameOverException:
                break

        g.print_grid()

        if g.unit_counts['E'] == initial_elves:
            break

        elf_power += 1

    print(elf_power)

    return g.rounds * sum([u.hit_points for u in g.units])
