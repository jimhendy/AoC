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
            pass
        else:
            new_dir = Droid.random_direction()
            droid(new_dir)
            pass
        
        if count % 100 == 0:
            droid.plot(True)
            pass

        count += 1
        pass

    route = droid.droid_route(np.array([0, 0]))

    return len(route)
