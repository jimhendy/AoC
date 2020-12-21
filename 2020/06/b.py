import os
import string

def run(inputs):
    '''
    inputs = inputs.split("\n\n")

    numTrue = 0

    for group in inputs:
        num = len(group.split("\n"))
        for question in string.ascii_letters[:26]:
            if group.count(question) == num:
                numTrue += 1

    return numTrue
    '''
    
    total = 0
    data = None  # We will use a set to store the letters again but need a special way of knowing when we are starting a new group. Note: len(data) == 0 is not valid as then we can't tell between a new group and an existing group with no overlapping answers
    for line in inputs.split(os.linesep):

        line = line.strip()

        if not len(line):
            # Reaching an empty line means a new group so add the current total and reset
            total += len(data)
            data = None
        else:
            if data is None:
                # The first person in the group, add all their answers to data and make it a set
                data = set(list(line))
            else:
                # Another person in the same group, add their letters to the set only if they are already present
                data = data.intersection(set(list(line)))

    # We may still have some un-counted results for the final group if the input did not end on a blank line, otherwise we will add zero below
    total += len(data)

    return total
    
