import re
import queue
import time
from droid import Droid, Direction
import numpy as np
from functools import lru_cache

def match_reg(arr, reg):
    matcher = np.vectorize(lambda x: bool(reg.match(x)))
    return matcher(arr)

def possibles_with_keys(arr, keys):
    reg = re.compile('^[\.\@a-z' + ''.join([i.upper() for i in keys]) + ']$')
    return match_reg(arr, reg)

def key_map(arr, unvisited):
    reg = re.compile('^[a-z]$')
    visited = arr[~unvisited]
    return visited[match_reg(visited, reg)]


d_cache = {}

def dijkstra(droid, origin, destination, return_route=True):
    global d_cache

    key = tuple((tuple(origin), tuple(destination)))
    if key in d_cache.keys():
        return d_cache[key]
    
    unvisited = np.full(droid.layout.shape, True)
    possibles = possibles_with_keys(droid.layout, [])
    unvisited[tuple(origin.astype(int))] = False
    keys = key_map(droid.layout, unvisited)
    
    steps = 0

    while True:
        if unvisited[tuple(destination.astype(int))] == False:
            # Found the destination
            break
        if all(~unvisited[possibles]):
            #print('Unable to find the destination')
            return False
        # Expand the unvisited map if possible
        next_unvisited = np.all(
            [unvisited] + [
                np.roll(unvisited, r, axis=a)
                for r in [-1, 1]
                for a in [0, 1]
            ],
            axis=0
        )
        next_unvisited[~possibles] = True
        if np.array_equal(unvisited, next_unvisited):
            #print(unvisited)
            #print('Nowhere to take the next step')
            #import code
            #code.interact(local=locals())
            return False
        unvisited = next_unvisited
        steps += 1

        available_keys = key_map(droid.layout, unvisited)
    
        possibles = possibles_with_keys(droid.layout, available_keys)
        
        pass

    if return_route:
        route = list(Droid.find_route(
            destination,
            origin,
            np.argwhere(~unvisited)
        )[::-1])
        d_cache[key] = route
        return route
    else:
        return steps
    pass


def route_to_str(route):
    return ''.join(list(map(str, route)))


def str_to_route(string):
    return [Direction(int(i)) for i in list(string)]


def is_valid_pos(droid, route):
    droid.reset()
    try:
        """
        for r in route:
            droid.go_to(r)
            droid.plot(True)
            time.sleep(0.01)
        """
        [droid.go_to(r) for r in route]
    except Exception as e:
        #    print(e)
        return False
    return True


def is_complete(droid, route):
    droid.reset()
    [droid.go_to(r) for r in route]
    # Find number of remaining keys
    ascii_ = np.array([[ord(j) for j in i] for i in droid.layout])
    key_pos = np.argwhere((ascii_ >= 97) & (ascii_ <= 122))
    return len(key_pos) == 0


def opposite_direction(direction):
    return {
        Direction.NORTH: Direction.SOUTH,
        Direction.SOUTH: Direction.NORTH,
        Direction.EAST: Direction.WEST,
        Direction.WEST: Direction.EAST
    }[direction]


def run(inputs):

    droid = Droid(inputs)
    droid.plot()

    interesting_reg = re.compile('^[^\.\@\#A-Z]$')
    interesting_points = np.argwhere( match_reg(droid.layout, interesting_reg) )
    
    possibles_q=queue.Queue()
    # List of move destinations
    destinations=[droid.get_current_position()]
    possibles_q.put(destinations)

    print(interesting_points)
    
    while not is_complete(droid, route_from_destinations(droid, destinations)):
        destinations = possibles_q.get()
        #print(route)
        for new_destination in interesting_points:
            if np.any(np.all(np.array(destinations) == new_destination, axis=1)):
                print('Bad')
                print(destinations, new_destination)
                continue
            extra_route = dijkstra(droid, destinations[-1], new_destination, return_route=True)
            if extra_route is False:
                print(False)
                print(destinations[-1], new_destination)
                print('-')
                continue
            new_destinations = destinations + [new_destination]
            print(new_destinations)
            #print(new_destinations)
            route = route_from_destinations(droid, new_destinations)
            if is_valid_pos(droid, route):
                # droid.plot(True)
                #print(attempt, new_route[:])
                # time.sleep(0.1)
                possibles_q.put(new_destinations)
                pass
            pass
        pass

    import code
    code.interact(local=locals())

    return 0

rfd_cache = {}
def route_from_destinations(droid, destinations):
    global rfd_cache
    key = str(destinations)
    if key in rfd_cache.keys():
        return rfd_cache[key]
    if len(destinations) == 1:
        return destinations
    route = [
        dijkstra(droid, destinations[i], destinations[i+1], return_route=True)
        for i in range(len(destinations)-1)
    ]
    route = np.array([ i for j in route for i in j ])
    route = route[np.hstack([[True], np.abs(np.diff(route, axis=0)).sum(axis=1)!=0])]
    assert np.all(np.abs(np.diff(route, axis=0)).sum(axis=1)==1)
    rfd_cache[key] = route[:]
    return route
