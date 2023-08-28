import os

from jumpcode import JumpCode


def bail_func(self):
    if len(self.recovered_sounds):
        return self.recovered_sounds[0]
    return None


def run(inputs):
    code = JumpCode(inputs.split(os.linesep), bail_func=bail_func)
    return code.run()
