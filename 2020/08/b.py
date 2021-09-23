import os
from bootcode import BootCode


def run(inputs):
    ins = inputs.split(os.linesep)

    for i in range(len(ins)):
        ins_copy = ins[:]
        if ins_copy[i].startswith("nop"):
            ins_copy[i] = ins_copy[i].replace("nop", "jmp")
        elif ins_copy[i].startswith("jmp"):
            ins_copy[i] = ins_copy[i].replace("jmp", "nop")
        else:
            continue

        bc = BootCode(ins_copy)
        result = bc.run()

        if result is None:
            return bc.accumulator
