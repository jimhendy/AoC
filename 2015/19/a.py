import os
import re


def replace_str(in_str, remove, replace):
    index = -1
    start = 0

    while True:
        try:
            new_index = in_str.index(remove, start)
            if index == new_index:
                break
            index = new_index
            yield in_str[:index] + replace + in_str[index + len(remove) :]
            start = index + 1
            pass
        except ValueError:
            break
        pass

    pass


def run(inputs):

    reg = re.compile("(\D+) \=\> (\D+)")

    base = inputs.split(os.linesep)[-1]
    replacements = []
    for i in inputs.split(os.linesep):
        match = reg.findall(i)
        for m in match:
            replacements.append((m[0], m[1]))
            pass
        pass

    output = set()

    for r in replacements:
        for new_chem in replace_str(base, r[0], r[1]):
            output.add(new_chem)
            pass
        pass

    return len(output)
