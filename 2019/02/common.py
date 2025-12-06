import numpy as np


def in_to_array(inputs):
    return np.array(inputs.split(",")).astype(int)


def intcode(inputs):
    in_copy = inputs.copy()
    address = 0
    while True:
        ret_value, ret_address, step = analyse_optcode(in_copy, address)
        if ret_address is None:
            break
        in_copy[ret_address] = ret_value
        address += step
    return in_copy


def analyse_optcode(inputs, address):
    if inputs[address] == 99:
        return None, None, 1
    if inputs[address] == 1:
        return add(inputs, address)
    if inputs[address] == 2:
        return mul(inputs, address)
    print(inputs)
    print(inputs[address : address + 4])
    msg = f'Unexpected code "{inputs[address]}" at address "{address}"'
    raise NotImplementedError(
        msg,
    )


def add(inputs, address):
    return (
        inputs[inputs[address + 1]] + inputs[inputs[address + 2]],
        inputs[address + 3],
        4,
    )


def mul(inputs, address):
    return (
        inputs[inputs[address + 1]] * inputs[inputs[address + 2]],
        inputs[address + 3],
        4,
    )
