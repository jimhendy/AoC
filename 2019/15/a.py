import numpy as np
from droid import Droid

np.random.seed(123)


def run(inputs):
    droid = Droid(inputs)

    count = 0
    while droid.tank_position is None:
        new_dir = None
        layout = droid.get_layout()

        if len(layout) > 1:
            new_pos = droid.find_unknown_cell(layout)
            droid.go_to(new_pos, layout)
        else:
            new_dir = Droid.random_direction()
            droid(new_dir)

        if count % 100 == 0:
            droid.plot(True)

        count += 1

    route = droid.droid_route(np.array([0, 0]))

    return len(route)
