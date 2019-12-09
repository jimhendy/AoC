import common


def run(inputs):

    prog = common.optprog(inputs)
    prog.analyse_intcode(1)

    return prog.outputs[-1]
