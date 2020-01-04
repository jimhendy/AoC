import os
import heapq
import collections
import numpy as np

STEPS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def get_char(grid, loc):
    return grid[loc[1]][loc[0]]


def reachable_keys(loc, keys, grid):
    q = collections.deque([(loc, 0)])
    seen = set()
    while q:
        loc, num_steps = q.popleft()
        new_char = get_char(grid, loc)
        if new_char.islower() and new_char not in keys:
            yield num_steps, loc, new_char
            continue
        for s in STEPS:
            new_loc = loc[0]+s[0], loc[1]+s[1]
            if (new_loc) in seen:
                continue
            seen.add(new_loc)
            new_char = get_char(grid, new_loc)
            if new_char != '#' and (not new_char.isupper()) or (new_char.lower() in keys):
                q.append((new_loc, num_steps+1))


def run(inputs):
    grid = inputs.split(os.linesep)
    droid_loc = [(x, y) for y, row in enumerate(grid)
                 for x, char in enumerate(row) if char == '@'][0]
    all_keys = set([char for y, row in enumerate(grid)
                    for x, char in enumerate(row) if char.islower()])

    # Fix the grid
    grid[droid_loc[1]-1] = grid[droid_loc[1]-1][:droid_loc[0]] + \
        '#' + grid[droid_loc[1]-1][droid_loc[0]+1:]
    grid[droid_loc[1]] = grid[droid_loc[1]][:droid_loc[0]-1] + \
        '###' + grid[droid_loc[1]][droid_loc[0]+2:]
    grid[droid_loc[1]+1] = grid[droid_loc[1]+1][:droid_loc[0]] + \
        '#' + grid[droid_loc[1]+1][droid_loc[0]+1:]

    pos = (
        ( droid_loc[0]-1, droid_loc[1]-1),
        ( droid_loc[0]+1, droid_loc[1]-1),
        ( droid_loc[0]-1, droid_loc[1]+1),
        ( droid_loc[0]+1, droid_loc[1]+1)
    )
    
    q = [(0, pos, frozenset())]
    seen = [set(), set(), set(), set()]

    while q:
        steps, locs, keys = heapq.heappop(q)
        if keys == all_keys:
            return steps
        for i, loc in enumerate(locs):
            if (loc, keys) in seen[i]:
                continue
            seen[i].add((loc, keys))
            for new_steps, new_loc, new_key in reachable_keys(loc, keys, grid):
                new_locs = locs[:i] + (new_loc,) + locs[i+1:]
                print(new_locs)
                heapq.heappush(q, (steps+new_steps, new_locs,
                                   keys | frozenset([new_key])))
