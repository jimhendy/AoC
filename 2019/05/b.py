import common

def run(inputs):
    prog = common.optprog(inputs)
    prog.analyse_intcode()
    return prog.outputs[-1]
    
    
