import ast
import os


def run(inputs):
    code = 0
    memory = 0

    for i in inputs.split(os.linesep):
        code += len(i)
        memory += len(ast.literal_eval(i))
        pass

    return code - memory
