import re
import common
import pandas as pd

def run(inputs):
    possibles = common.possibles(inputs)
    diffs = common.diffs(possibles)
    counts = common.counts(possibles)

    diffs_mask = diffs.gt(-1).all(axis=1)
    counts_mask = counts.gt(1).any(axis=1)
    
    diff_str = pd.Series(0, index=possibles.index)
    for i in range(diffs.shape[1]-1):
        col = diffs.astype(int).iloc[:,i+1]
        diff_str += col.abs().mul(10**(diffs.shape[1]-2-i))
        pass
    diff_str = diff_str.astype(str)
    
    zeros_mask = (
        diff_str.str.contains('[^0]0[^0]')
        |
        diff_str.str.contains('0[^0]$')
        |
        diff_str.str.contains('$0[^0]')
    )
    
    possibles = possibles[
        diffs_mask & counts_mask & zeros_mask
    ]
    
    return len(possibles)
        
