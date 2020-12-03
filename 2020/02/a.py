import os
import re

def run(inputs):
    reg = re.compile(r'(\d+)\-(\d+) ([a-zA-Z])\: ([a-zA-Z]+)')
    total = 0
    for l in inputs.split(os.linesep):
        match = reg.findall(l)[0]
        count = match[3].count(match[2])
        if (int(match[0])<=count) and (count<=int(match[1])):
            total += 1
    return total