import os
import re

REGS = {
    "not": re.compile(r"NOT (.+) \-\> (\D+)"),
    "shift": re.compile(r"(.+) [LR]SHIFT (\d+) \-\> (\D+)"),
    "and": re.compile(r"(.+) AND (.+) \-\> (\D+)"),
    "or": re.compile(r"(.+) OR (.+) \-\> (\D+)"),
    "direct": re.compile(r"(.+) \-\> (\D+)"),
}


def get_num(key, wires):
    if key.isdigit():
        return int(key)
    return int(wires[key])


def ret_value(line, wires, reg, func):
    data = reg.findall(line)[0]
    nums = [get_num(data[i], wires) for i in range(len(data) - 1)]
    return data[-1], func(nums)


def do_not(line, wires):
    return ret_value(line, wires, REGS["not"], lambda x: ~x[0])


def do_and(line, wires):
    return ret_value(line, wires, REGS["and"], lambda x: x[0] & x[1])


def do_or(line, wires):
    return ret_value(line, wires, REGS["or"], lambda x: x[0] | x[1])


def do_l_shift(line, wires):
    return ret_value(line, wires, REGS["shift"], lambda x: x[0] << x[1])


def do_r_shift(line, wires):
    return ret_value(line, wires, REGS["shift"], lambda x: x[0] >> x[1])


def do_direct(line, wires):
    return ret_value(line, wires, REGS["direct"], lambda x: x[0])


def run_once(wires, inputs, skip=[]):
    inputs = inputs.split(os.linesep)
    remaining_inputs = inputs[:]

    while len(remaining_inputs):

        inputs = remaining_inputs[:]

        for line in inputs:
            func = None
            if " AND " in line:
                func = do_and
            elif " OR " in line:
                func = do_or
            elif "NOT " in line:
                func = do_not
            elif " RSHIFT " in line:
                func = do_r_shift
            elif " LSHIFT " in line:
                func = do_l_shift
            else:
                func = do_direct
                pass

            try:
                loc, value = func(line, wires)
                if not any([loc == i for i in skip]):
                    wires[loc] = value
                    pass
                remaining_inputs.remove(line)
                pass
            except KeyError:
                continue

            pass

        pass
    return wires


def run(inputs):
    wires = {}
    run_once(wires, inputs)
    wires = {"b": wires["a"]}
    second = run_once(wires, inputs, ["b"])
    return second["a"]
