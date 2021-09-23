import os
import common


def run(inputs):

    all_reactions = tuple([common.Reaction(r) for r in inputs.split(os.linesep)])
    fuel_reaction = common.find_reaction(all_reactions, "FUEL")

    store = common.run_reaction(fuel_reaction, all_reactions)

    return store._used_store["ORE"]
