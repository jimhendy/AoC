import os
import re


def run(inputs):

    code = 0
    memory = 0

    for i in inputs.split(os.linesep):
        code += len(i)
        memory += len(re.escape(i)) + 2
        pass

    return memory - code
