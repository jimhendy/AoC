import os

import common
import numpy as np


def run(inputs):
    all_reactions = tuple([common.Reaction(r) for r in inputs.split(os.linesep)])
    fuel_reaction = common.find_reaction(all_reactions, "FUEL")
    initial_ore = 1e12

    def num_ore(num_fuel):
        store = common.Store()
        common.run_reaction(fuel_reaction * num_fuel, all_reactions, store)
        return store._used_store["ORE"]

    # The first time we get no freebies so this is
    # the max possible ore used to produce 1 fuel
    max_ore_per_fuel = num_ore(1)
    min_possible_fuels = initial_ore / max_ore_per_fuel

    left = int(min_possible_fuels)
    right = int(left * 2)

    while left <= right:
        mid = int(np.floor(left + (right - left) / 2))

        ore = num_ore(mid)
        if ore > initial_ore:
            right = mid - 1
        elif ore < initial_ore:
            left = mid + 1

    return right
