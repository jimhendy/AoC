import os

def run(inputs):
    total = 0
    for row in inputs.split(os.linesep):
        seen = set()
        valid = 1
        for word in row.split():
            sword = ''.join(sorted(word))
            if sword in seen:
                valid = 0
                break
            seen.add(sword)
        total += valid
    return total
        