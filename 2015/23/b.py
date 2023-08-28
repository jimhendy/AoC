import os

import computer


def run(inputs):
    comp = computer.Computer(inputs.split(os.linesep))
    comp.a = 1
    comp.run()

    return comp.b
