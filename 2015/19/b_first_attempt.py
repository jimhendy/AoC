import os
import re
from collections import defaultdict

from cyk import cyk


def run(inputs):
    raw_base = inputs.split(os.linesep)[-1]
    base = re.compile("([A-Z](?:[a-z]*))").findall(raw_base)

    reaction_reg = re.compile(r"(\D+) \=\> (\D+)")
    reactions = defaultdict(set)
    for i in inputs.split(os.linesep):
        match = reaction_reg.findall(i)
        for m in match:
            reactions[m[0]].add(m[1])
            pass
        pass

    cyk(base, reactions)
