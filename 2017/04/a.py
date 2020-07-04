import os

def run(inputs):
    total = 0
    for row in inputs.split(os.linesep):
        seen = set()
        valid = 1
        for word in row.split():
            if word in seen:
                valid = 0
                break
            seen.add(word)
        total += valid
    return total
        