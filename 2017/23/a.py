import os
from jumpcode import JumpCode


def run(inputs):
    code = JumpCode(inputs.split(os.linesep), debug_mode=True)
    code.run()
    return code.instruction_nums["mul"]
