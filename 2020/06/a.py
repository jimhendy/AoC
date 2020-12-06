import os

def run(inputs):

    total = 0
    data = set()
    for line in inputs.split(os.linesep):
        if not len(line.strip()):
            total += len(data)
            data = set()
        else:
            for letter in list(line.strip()):
                data.add(letter)

    total += len(data)

    return total