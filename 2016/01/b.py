import numpy as np

steps = {
    "W": np.array([-1, 0]),
    "E": np.array([+1, 0]),
    "N": np.array([0, -1]),
    "S": np.array([0, +1]),
}

dirs = ["N", "E", "S", "W"]


def add_loc(locs, loc):
    locs.add(tuple(loc))
    return locs


def run(inputs):
    direction = "N"
    loc = np.array([0, 0])
    current_dir_it = dirs.index(direction)

    locs = set()
    locs = add_loc(locs, loc)

    for d in [j.strip() for j in inputs.split(",")]:
        turn = d[0]
        n_steps = int(d[1:])

        if turn == "R":
            step = 1
        elif turn == "L":
            step = -1
        else:
            raise NotImplementedError

        new_dir_it = (current_dir_it + step) % len(dirs)
        new_dir = dirs[new_dir_it]

        for _i in range(n_steps):
            loc += steps[new_dir]
            if tuple(loc) in locs:
                return np.abs(loc).sum()
            locs = add_loc(locs, loc)
            pass

        direction = new_dir
        current_dir_it = new_dir_it

        pass

    return np.abs(loc).sum()
