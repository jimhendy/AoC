import optcode
import os

def run(inputs):
    
    # Two blank lines indicate start of code
    instructions = []
    start = False
    prev_line = 'start'
    for l in inputs.split(os.linesep):
        if start and len(l.strip()):
            instructions.append(l)
        if not len(l.strip()) and not len(prev_line.strip()):
            start = True
        prev_line = l

    oc = optcode.OptCode(instructions)
    oc.run()

    return oc.registers[0]