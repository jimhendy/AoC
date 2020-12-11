import os


def run(inputs):

    total = 0
    data = None
    for line in inputs.split(os.linesep):

        line = line.strip()

        if not len(line):
            total += len(data)
            data = None
        else:
            if data is None:
                data = set(list(line))
            else:
                data = data.intersection(set(list(line)))

    total += len(data)

    return total
