from intcode import Intcode
import os


def instruction(instr, prog):
    [prog.analyse_intcode(ord(i)) for i in list(instr)]
    prog.analyse_intcode(10)
    pass


def run(inputs):

    prog = Intcode(inputs)

    ins = [
        'NOT B J',
        'NOT C T',
        'OR J T',
        'AND D T',
        'NOT A J',
        'OR T J',
        'WALK'
    ]

    [instruction(i, prog) for i in ins]
    [
        print(i)
        for i in ''.join(
                [
                    chr(i)
                    for i in prog.outputs[:-1]
                ]
        ).split(os.linesep)
    ]
    return prog.outputs[-1]
