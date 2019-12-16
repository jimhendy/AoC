import tqdm
import numpy as np

BASE_PATTERN = [0,1,0,-1]

def run_phase(inp, phase):
    data = np.array([ int(i) for i in list(inp) ])
    pattern_data = []
    for i in tqdm.tqdm(range(data.shape[0])):
        pat = np.repeat(BASE_PATTERN, i+1)
        pat = np.tile( pat, int(np.ceil(data.shape[0]/pat.shape[0])) + 1 )[1:data.shape[0]+1]
        pattern_data.append(np.mod(np.abs((data * pat).sum()),10))
        pass
    import code
    code.interact(local=locals())
    return ''.join([str(i) for i in ans]).zfill(data.shape[0])

def run(inputs):

    phase = 0
    inp = inputs * 10000

    offset = inputs[:8]
    
    for phase in tqdm.tqdm(range(100)):
        inp = run_phase(inp, phase)
        pass

    return inp[offset:8]
