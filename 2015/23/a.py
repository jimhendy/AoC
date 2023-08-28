import os

import computer


def run(inputs):
    comp = computer.Computer(inputs.split(os.linesep))
    comp.run()

    return comp.b
