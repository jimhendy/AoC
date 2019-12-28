import os

def run(inputs):

    cards = list( range(10) )

    instructions = []
    for i in inputs.split(os.linesep):
        ins = '_'.join(i.split())
        if ins[-1].isdigit():
            ins = '_'.join(ins.split('_')[:-1]), int(ins.split('_')[-1])
            pass
        instructions.append(ins)
        pass
    
    import code
    code.interact(local=locals())
