import re


def run(inputs):

    # Remove double !!
    while "!!" in inputs:
        inputs = re.sub("\!\!", "", inputs)

    # Remove cancelled characters
    inputs = re.sub("\!.", "", inputs)

    # Remove garbage
    inputs = re.sub("(<.*?>)", "", inputs)

    level = 0
    total = 0
    for c in inputs:
        if c == "{":
            level += 1
        elif c == "}":
            total += level
            level -= 1

    return total
