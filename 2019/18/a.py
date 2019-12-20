import re
import queue
import time
import numba
from droid import Droid, Direction, move
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
    return list(visited[match_reg(visited, reg)])

@numba.njit
def expand_unvisited(unvisited):
    visited = ~ unvisited
    down = np.roll(visited.T,1).T
    up = np.roll(visited.T,-1).T
    right = np.roll(visited,1)
    left = np.roll(visited,-1)
    result = visited + up + down + left + right
    return ~result            

d_cache = {}
@profile
def dijkstra(droid, origin, destination, starting_keys = []):
    global d_cache

    droid.reset()
    
    key = f'{origin}{destination}{starting_keys}'
    if key in d_cache.keys():
        return d_cache[key]

    unvisited = np.full(droid.layout.shape, True)
    possibles = possibles_with_keys(droid.layout, starting_keys)
    unvisited[tuple(origin.astype(int))] = False
    #keys = key_map(droid.layout, unvisited)

    parents = {}
    pos_steps = [ Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST ]
    steps = 0

    while True:

        if unvisited[tuple(destination.astype(int))] == False:
            # Found the destination
            break

        if all(~unvisited[possibles]):
            #print('Unable to find the destination')
            return False

        # Expand the unvisited map if possible
        next_unvisited = expand_unvisited(unvisited)
        """
        np.all(
            [unvisited] + [
                np.roll(unvisited, r, axis=a)
                for r in [-1, 1]
                for a in [0, 1]
            ],
            axis=0
        )
        """
        next_unvisited[~possibles] = True

        newly_visited = np.argwhere( (unvisited==True) & (next_unvisited==False) )
        for new_c in newly_visited:
            for step in pos_steps:
                pos_old_pos = move(new_c, step)
                if np.any(pos_old_pos<0):
                    continue
                if np.any(pos_old_pos>unvisited.shape):
                    continue
                if unvisited[tuple(pos_old_pos.astype(int))] == False:
                    parents[tuple(new_c.astype(int))] = pos_old_pos
                    break
                pass
            pass
                
        if np.array_equal(unvisited, next_unvisited):
            #print('Nowhere to take the next step')
            return False

        unvisited = next_unvisited
        steps += 1
        #available_keys = key_map(droid.layout, unvisited)
        #possibles = possibles_with_keys(droid.layout, starting_keys + available_keys)
        
        pass

    route = [destination]
    while not np.all(route[-1] == origin):
        route.append(parents[tuple(route[-1].astype(int))])
        pass
    route = route[::-1]

    picked_up_keys = key_map(droid.layout, unvisited)
    d_cache[key] = route, picked_up_keys
    return route, picked_up_keys




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
        print(destinations)
        for new_destination in interesting_points:
            if np.any(np.all(np.array(destinations) == new_destination, axis=1)):
                #print('Bad')
                #print(destinations, new_destination)
                continue

            new_destinations = destinations + [new_destination]
            #print(new_destinations)
            #print(new_destinations)
            route = route_from_destinations(droid, new_destinations)
            if route is False:
                continue
            
            if is_valid_pos(droid, route):
                #print(new_destinations)
                #print('--- y')
                # droid.plot(True)
                #print(attempt, new_route[:])
                # time.sleep(0.1)
                possibles_q.put(new_destinations)
                pass
            else:
                #print('N')
                pass
            #print('+'*8)
            pass
        pass

    return len(route) - 1

rfd_cache = {}
def route_from_destinations(droid, destinations):
    global rfd_cache
    key = str(destinations)
    if key in rfd_cache.keys():
        return rfd_cache[key]
    if len(destinations) == 1:
        return destinations

    prev_keys = []
    route = [destinations[0]]
    #print(destinations)
    for end in destinations[1:]:

        start = route[-1]
        
        if len(route) and np.any( np.all(end==np.array(route), axis=1) ):
            # Already visited this destination
            continue
        
        #print(prev_keys)
        new_route = dijkstra(droid, start, end, prev_keys)
        if new_route == False:
            #print(False)
            return False
        new_route, prev_keys = new_route
        #print(prev_keys)
        #print('-')
        route.extend(new_route)
        pass
    
    route = np.array(route)
    route = route[np.hstack([[True], np.abs(np.diff(route, axis=0)).sum(axis=1)!=0])]
    assert np.all(np.abs(np.diff(route, axis=0)).sum(axis=1)==1)
    rfd_cache[key] = route.copy()
    return route
