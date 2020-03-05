import re
import os
import heapq
from collections import defaultdict


class Molecule():
    def __init__(self, n_reacts, mol_str, reacts):
        self.n_reacts = n_reacts
        self.mol_str = mol_str
        self.reacts = reacts
        pass

    def size(self):
        return self.n_reacts + len(self.mol_str)

    def __gt__(self, other):
        return self.size() > other.size()

    def __lt__(self, other):
        return not self.__gt__(other)


def replace_all(string, drop, insert):
    for c in range(string.count(drop)):
        where = [m.start() for m in re.finditer(drop, string)][c-1]
        before = string[:where]
        after = string[where:]
        after = after.replace(drop, insert, 1)
        yield before + after


def run(inputs):

    base = inputs.split(os.linesep)[-1]

    reaction_reg = re.compile('(\D+) \=\> (\D+)')
    reactions = defaultdict(set)
    for i in inputs.split(os.linesep):
        match = reaction_reg.findall(i)
        for m in match:
            reactions[m[0]].add(m[1])
            pass
        pass

    possibles = [Molecule(0, base, [])]
    seen = set([base])
    total = 0
    
    while len(possibles):

        total += 1
        
        best_option = heapq.heappop(possibles)
        current_mol = best_option.mol_str

        if current_mol == 'e':
            break

        for start, ends in reactions.items():
            for end in ends:
                for new_mol in replace_all(current_mol, end, start):
                    if new_mol in seen:
                        continue
                    seen.add(new_mol)
                    heapq.heappush(
                        possibles,
                        Molecule(
                            best_option.n_reacts + 1,
                            new_mol,
                            best_option.reacts + [f'{start}=>{end}'])
                    )

    return best_option.n_reacts
