import os

from army import Army

def run(inputs):
    
    base_armies = []
    for line in inputs.split(os.linesep):
        if not line.strip():
            continue
        if line.endswith(':'):
            base_armies.append(Army(line.rstrip(':')))
        else:
            base_armies[-1].add_group(line)

    infection = [ a for a in base_armies if a.name == 'Infection'][0]
    immune_system = [ a for a in base_armies if a.name != 'Infection'][0]

    boost = 0
    while True:
        print('='*50)
        print(boost)
        armies = [infection.copy(), immune_system.boost(boost)]
        prev_units = None
        while all([len(a.groups) for a in armies]):
            n_units = sum([g.n_units for a in armies for g in a.groups])
            if n_units == prev_units:
                # Draw
                break
            prev_units = n_units
            #print([g.n_units for g in armies[0].groups])
            #print([g.immunities for g in armies[0].groups])
            #print([g.n_units for g in armies[1].groups])
            #print([g.attack_type for g in armies[1].groups])
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
                [ g for a in armies for g in a.groups ],
                key = lambda g : g.initiative
            )[::-1]
            for g in all_groups:
                g.attack()

            for a in armies:
                a.bring_out_your_dead()
        if len(armies[1].groups):
            return boost
        else:
            boost += 1