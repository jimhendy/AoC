import os

from intcode import Intcode


def instruction(instr, prog):
    [prog.analyse_intcode(ord(i)) for i in list(instr)]
    prog.analyse_intcode(10)


def run(inputs):
    prog = Intcode(inputs)

    ins = [
        # Either not B or not C
        "NOT B J",
        "NOT C T",
        "OR J T",
        # And D
        "AND D T",
        # Reset J to True
        "NOT T J",
        "OR T J",
        # E or H (next landing site)
        "AND E J",
        "OR H J",
        # All above
        "AND J T",
        # Need to jump if not A
        "NOT A J",
        "OR T J",
        "RUN",
    ]

    [instruction(i, prog) for i in ins]
    [print(i) for i in "".join([chr(i) for i in prog.outputs[:-1]]).split(os.linesep)]
    return prog.outputs[-1]
