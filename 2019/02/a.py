import common

def run(inputs):

    in_copy = common.in_to_array(inputs)

    in_copy[1] = 12
    in_copy[2] = 2
    output = common.intcode(in_copy)

    return output[0]
