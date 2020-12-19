import os

def run(inputs):

    total = 0
    data = set() # Use a set to store the answers from each group
    for line in inputs.split(os.linesep):
        if not len(line.strip()):
            # Reaching an empty line means a new group so add the current total and reset
            total += len(data)
            data = set()
        else:
            for letter in list(line.strip()):
                # Add each letter to the current group's answers
                # As data is a set we don't have to worry about duplicates
                data.add(letter)

    # We may still have some un-counted results for the final group if the input did not end on a blank line, otherwise we will add zero below
    total += len(data)

    return total