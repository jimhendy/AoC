import re
import os
import heapq
import numba

def replace_str(in_str, remove, replace):
    splits = in_str.split(remove)
    for i in range(1,len(splits)):
        yield remove.join(splits[:i]) + replace + remove.join(splits[i+1:])
        pass
    pass

def run(inputs):
    
    reg = re.compile('(\D+) \=\> (\D+)')

    base = inputs.split(os.linesep)[-1]
    replacements = []
    for i in inputs.split(os.linesep):
        match = reg.findall(i)
        for m in match:
            replacements.append( (m[0], m[1]) )
            pass
        pass

    q = [(0, 'e')]
    seen = set()
    
    while len(q):
        steps, possible = heapq.heappop(q)
        if possible in seen:
            continue
        seen.add(possible)
        if possible == base:
            return steps
        #print(possible)
        for r in replacements:
            for new_possible in replace_str(possible, r[0], r[1]):
                if len(new_possible) <= len(base):
                    heapq.heappush(q, (steps+1, new_possible) )

        
    
