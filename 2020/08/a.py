import os
from bootcode import BootCode


def run(inputs):
    ins = inputs.split(os.linesep)
    bc = BootCode(ins)
    return bc.run()
