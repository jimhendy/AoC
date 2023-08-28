import numba
import numpy as np
from droid import Direction, MapSymbol, move

completed_tiles = []


def find_unknown_cell(layout):
    global completed_tiles
    pos, content = layout
    path_mask = (content == MapSymbol.PREVIOUS) | (content == MapSymbol.DROID)
    path = pos[path_mask]
    pos[:, 0]
    pos[:, 1]
    for p in path[::-1]:
        if tuple(p) in completed_tiles:
            continue
        for step in [Direction.NORTH, Direction.EAST, Direction.WEST, Direction.SOUTH]:
            new_pos = move(p, step)
            point_index = array_match_mask(pos, new_pos)
            if any(point_index):
                if all(content[point_index] == MapSymbol.UNKNOWN):
                    return new_pos
                else:
                    continue
                pass
            else:
                return new_pos
            pass
        completed_tiles.append(tuple(p))
        pass
    return False


def random_direction():
    dir_int = np.random.randint(1, 5)
    return Direction(dir_int)


@numba.njit
def arrays_match(a, b):
    return np.all(a == b)


def array_match_mask(possibles, arr):
    return np.all(possibles == arr, axis=1)


def remove_array(possibles, arr):
    return possibles[~array_match_mask(possibles, arr)]


def remove_nan_rows(arr):
    return arr[~np.isnan(arr.sum(axis=1))]


def find_route(origin, destination, possibles):
    route = np.full(possibles.shape, np.nan)
    route[0] = origin.copy()

    remaining_poss = possibles.copy()
    current_pos = origin.copy()
    current_route_it = 1

    while True:
        # If done, return
        if arrays_match(route[current_route_it - 1], destination):
            return remove_nan_rows(route)

        # Ensure we can't step back where we came from
        remaining_poss = remove_array(remaining_poss, current_pos)

        # Possible next steps are next to current position
        poss = remaining_poss[np.abs(remaining_poss - current_pos).sum(axis=1) == 1]

        if not len(poss):
            # No possible steps
            return False
        if len(poss) == 1:
            # Single option
            new_pos = poss[0].copy()
            route[current_route_it] = new_pos
            current_route_it += 1
            current_pos = new_pos
            pass
        else:
            # Multiple options

            # Sort the steps so we first go to the one which is closer
            # in Manhatten distance to the destination
            poss = sorted(poss, key=lambda x: np.abs(x - destination).sum())

            poss_next = remaining_poss.copy()
            for p in poss:
                if not len(poss_next):
                    pass
                it_route = find_route(p, destination, poss_next)
                if it_route is False:
                    continue
                route[current_route_it : current_route_it + len(it_route)] = it_route
                return remove_nan_rows(route)
            return False
            pass
        pass
    pass
    return None


def droid_route(droid, destination, layout=None):
    if layout is None:
        layout = droid.get_layout()
        pass

    pos, content = layout

    mask = (content == MapSymbol.DROID) | (content == MapSymbol.PREVIOUS)
    possible_pos = pos[mask]

    if not any(np.all(possible_pos == destination, axis=1)):
        possible_pos = np.vstack([possible_pos, destination])
        pass

    return find_route(droid.position, destination, possible_pos)


def go_to(droid, layout, destination):
    route = droid_route(droid, destination, layout)

    if route is False:
        msg = f"Cannot find route from {droid.position} to {destination}"
        raise Exception(msg)

    for r in route[1:]:
        if r[0] > droid.position[0]:
            yield Direction.EAST
        elif r[0] < droid.position[0]:
            yield Direction.WEST
        elif r[1] > droid.position[1]:
            yield Direction.NORTH
        elif r[1] < droid.position[1]:
            yield Direction.SOUTH
        else:
            raise NotImplementedError
        pass
    pass
