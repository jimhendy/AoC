import numpy as np

BASE_PATTERN = [0,1,0,-1]

def run_phase(inp, phase):
    data = np.array([ int(i) for i in list(inp) ])
    data = np.tile( data, data.shape[0] ).reshape(data.shape[0],-1)
    pattern_data = []
    for i in range(data.shape[0]):
        pat = np.repeat(BASE_PATTERN, i+1)
        pat = np.tile( pat, int(np.ceil(data.shape[0]/pat.shape[0])) + 1 )[1:data.shape[0]+1]
        pattern_data.append(pat)
        pass
    pattern = np.concatenate(pattern_data).reshape( data.shape )
    ans = np.mod( np.abs((data * pattern).sum(axis=1)), 10)
    return ''.join([str(i) for i in ans]).zfill(data.shape[0])

def run(inputs):

    phase = 0
    inp = inputs
    
    for phase in range(100):
        inp = run_phase(inp, phase)
        pass

    return inp[:8]
