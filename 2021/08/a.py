import os


def run(inputs):
    total = 0
    good_counts = {2, 3, 4, 7}
    for line in inputs.split(os.linesep):
        counts = map(len, line.split("|")[1].split())
        for c in counts:
            total += c in good_counts
    return total
