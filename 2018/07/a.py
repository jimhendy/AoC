import os
import re
from collections import defaultdict

def run(inputs):
    order = defaultdict(list)
    for i in re.findall(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.', inputs):
        order[i[0]].append(i[1])
    
    all_steps = set(list(order.keys()) + [j for i in order.values() for j in i])
    
    complete = []
    incomplete = list(all_steps.copy())

    while len(complete) != len(all_steps):
        available = [
            s for s in all_steps 
            if s not in complete 
            and all(
                [
                    s not in order[k]
                    for k in all_steps
                    if k not in complete
                ]
            )
        ]
        chosen = min(available)
        complete.append(chosen)
        incomplete.remove(chosen)

    return ''.join(complete)

