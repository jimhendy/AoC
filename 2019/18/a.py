import collections
import heapq
import os

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
            new_loc = loc[0] + s[0], loc[1] + s[1]
            if (new_loc) in seen:
                continue
            seen.add(new_loc)
            new_char = get_char(grid, new_loc)
            if (
                new_char != "#"
                and (not new_char.isupper())
                or (new_char.lower() in keys)
            ):
                q.append((new_loc, num_steps + 1))


def run(inputs):
    grid = inputs.split(os.linesep)
    droid_loc = next(
        (x, y)
        for y, row in enumerate(grid)
        for x, char in enumerate(row)
        if char == "@"
    )
    all_keys = {
        char
        for y, row in enumerate(grid)
        for x, char in enumerate(row)
        if char.islower()
    }
    q = [(0, droid_loc, frozenset())]
    seen = set()

    while q:
        steps, loc, keys = heapq.heappop(q)
        if keys == all_keys:
            return steps
        print(len(q))
        if (loc, keys) in seen:
            continue
        seen.add((loc, keys))
        for new_steps, new_loc, new_key in reachable_keys(loc, keys, grid):
            heapq.heappush(q, (steps + new_steps, new_loc, keys | frozenset([new_key])))
    return None
