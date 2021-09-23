import re


def run(inputs):

    # Remove double !!
    while "!!" in inputs:
        inputs = re.sub("\!\!", "", inputs)

    # Remove cancelled characters
    inputs = re.sub("\!.", "", inputs)

    total = 0
    for m in re.findall("<(.*?)>", inputs):
        total += len(m)

    return total
