import numpy as np
from droid import Droid, MapSymbol

np.random.seed(123)


def run(inputs):
    droid = Droid(inputs)

    count = 0
    while True:
        new_dir = None
        layout = droid.get_layout()

        if len(layout) > 1:
            new_pos = droid.find_unknown_cell(layout)
            if new_pos is False:
                break
            droid.go_to(new_pos, layout)
            pass
        else:
            new_dir = Droid.random_direction()
            droid(new_dir)
            pass

        if count % 1 == 0:
            pass

        count += 1
        pass

    minutes = 0
    droid.layout[tuple(droid.tank_position)] = MapSymbol.OXYGEN
    while True:
        new_o_cells = droid.find_oxygen_adjacent_cells()
        for nc in new_o_cells:
            droid.layout[tuple(nc)] = MapSymbol.OXYGEN
            pass
        if not len(new_o_cells):
            break
        if minutes % 1 == 0:
            pass
        minutes += 1
        pass

    return minutes
