import os


def run(input_data):
    max_ = 0
    this_total = 0
    for line in input_data.split(os.linesep):
        line = line.strip()
        if line:
            this_total += int(line)
        else:
            if this_total > max_:
                max_ = this_total
            this_total = 0
    return max_
