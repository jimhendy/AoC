import re

def run(inputs):

    result = 0
    half_length = int(len(inputs)/2)
    for i in range(len(inputs)):
        compare_pos = (half_length + i) % len(inputs)
        if inputs[i] == inputs[compare_pos]:
            result += int(inputs[i])
    return result