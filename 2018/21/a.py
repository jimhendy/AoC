import os

from optcode import OptCode


def run(inputs):
    inputs = inputs.split(os.linesep)
    ip = int(inputs[0].split()[1])
    oc = OptCode(ip, inputs[1:])
    oc.registers[0] = 986758
    oc.run()
    return oc.registers[0]
