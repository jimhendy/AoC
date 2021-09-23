import os
from jumpcode import JumpCode


def run(inputs):
    code = JumpCode(inputs.split(os.linesep))
    code.run()
    return code.registers["h"]
