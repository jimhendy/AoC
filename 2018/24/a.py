import os

from army import Army


def run(inputs):
    armies = []
    for line in inputs.split(os.linesep):
        if not line.strip():
            continue
        if line.endswith(":"):
            armies.append(Army(line.rstrip(":")))
        else:
            armies[-1].add_group(line)

    while all(len(a.groups) for a in armies):
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
            [g for a in armies for g in a.groups],
            key=lambda g: g.initiative,
        )[::-1]
        for g in all_groups:
            g.attack()

        for a in armies:
            a.bring_out_your_dead()

    return sum([g.n_units for a in armies for g in a.groups])
