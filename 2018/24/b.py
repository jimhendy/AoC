import os

from army import Army
from binary_search import binary_search


def fight(boost, infection, immune_system):
    armies = [infection.copy(), immune_system.boost(boost)]
    prev_units = None
    while all([len(a.groups) for a in armies]):
        n_units = sum([g.n_units for a in armies for g in a.groups])
        if n_units == prev_units:
            # Draw
            return False
        prev_units = n_units
        a_groups = armies[0].groups[:]
        b_groups = armies[1].groups[:]
        for g in sorted(armies[0].groups)[::-1]:
            chosen_target = g.target_selection(b_groups)
            if chosen_target is not None:
                b_groups.remove(chosen_target)
        for g in sorted(armies[1].groups)[::-1]:
            chosen_target = g.target_selection(a_groups)
            if chosen_target is not None:
                a_groups.remove(chosen_target)

        all_groups = sorted(
            [g for a in armies for g in a.groups], key=lambda g: g.initiative
        )[::-1]
        for g in all_groups:
            g.attack()

        for a in armies:
            a.bring_out_your_dead()
    if len(armies[1].groups) and not len(armies[0].groups):
        return sum([g.n_units for g in armies[1].groups])
    else:
        return False


def run(inputs):

    base_armies = []
    for line in inputs.split(os.linesep):
        if not line.strip():
            continue
        if line.endswith(":"):
            base_armies.append(Army(line.rstrip(":")))
        else:
            base_armies[-1].add_group(line)

    infection = [a for a in base_armies if a.name == "Infection"][0]
    immune_system = [a for a in base_armies if a.name != "Infection"][0]

    def boolean_fight(boost):
        return bool(fight(boost, infection, immune_system))

    min_boost = binary_search(boolean_fight, lower=0)

    return fight(min_boost, infection, immune_system)
