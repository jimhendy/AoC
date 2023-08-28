import re
from collections import deque

import numpy as np


def V(*a):
    return np.array(a)


# What will you have after this turn? Sorted from resources to robots
def key(a):
    return tuple(a[0] + a[1]) + tuple(a[1])


def prune(x):
    return sorted(x, key=key)[-100:]


def parse(line: str):
    (
        blueprint_id,
        ore_for_ore,
        ore_for_clay,
        ore_for_obsidian,
        clay_for_obsidian,
        ore_for_geode,
        obsidian_for_geode,
    ) = map(int, re.findall(r"\d+", line))
    return (
        blueprint_id,
        (V(0, 0, 0, ore_for_ore), V(0, 0, 0, 1)),
        (V(0, 0, 0, ore_for_clay), V(0, 0, 1, 0)),
        (
            V(0, 0, clay_for_obsidian, ore_for_obsidian),
            V(0, 1, 0, 0),
        ),
        (
            V(0, obsidian_for_geode, 0, ore_for_geode),
            V(1, 0, 0, 0),
        ),
        (V(0, 0, 0, 0), V(0, 0, 0, 0)),
    )


def analyse_blueperint(blueprint, total_time: int) -> int:
    todo = [(V(0, 0, 0, 0), V(0, 0, 0, 1))]  # Resources and Robots
    for _ in range(total_time):
        next_timestep = deque()  # Queue for the next minute.
        for resources, robots in todo:
            for cost, new_robots in blueprint:
                if all(cost <= resources):  # We can afford this robot.
                    next_timestep.append(
                        (resources + robots - cost, robots + new_robots),
                    )
        todo = prune(next_timestep)  # Prune the search queue.
    return max(have[0] for have, _ in todo)


def run(inputs: str) -> int:
    return sum(
        analyse_blueperint(blueprint, 24) * i
        for i, *blueprint in [parse(line) for line in inputs.splitlines()]
    )
