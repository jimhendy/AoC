import re


def run(inputs):
    # Remove double !!
    while "!!" in inputs:
        inputs = re.sub(r"\!\!", "", inputs)

    # Remove cancelled characters
    inputs = re.sub(r"\!.", "", inputs)

    total = 0
    for m in re.findall("<(.*?)>", inputs):
        total += len(m)

    return total
