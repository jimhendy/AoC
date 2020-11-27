import os
from jumpcode import JumpCode

def run(inputs):
    code = JumpCode(inputs.split(os.linesep))
    code.run()
    import pdb; pdb.set_trace()
    return code.registers['h']