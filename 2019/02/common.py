import numpy as np

def in_to_array(inputs):
    return np.array(inputs.split(',')).astype(int)

def intcode(inputs):
    in_copy = inputs.copy()
    address = 0
    while True:
        ret_value, ret_address, step = analyse_optcode(in_copy, address)
        if ret_address is None:
            break
        in_copy[ret_address] = ret_value
        address += step
        pass
    return in_copy
        

def analyse_optcode(inputs, address):
    if inputs[address] == 99:
        return None, None, 1
    elif inputs[address] == 1:
        return add(inputs, address)
    elif inputs[address] == 2:
        return mul(inputs, address)
    else:
        print(inputs)
        print(inputs[address:address+4])
        raise NotImplementedError(f'Unexpected code "{inputs[address]}" at addressition "{address}"')

def add(inputs, address):
    return inputs[inputs[address+1]] + inputs[inputs[address+2]], inputs[address+3], 4


def mul(inputs, address):
    return inputs[inputs[address+1]] * inputs[inputs[address+2]], inputs[address+3], 4
