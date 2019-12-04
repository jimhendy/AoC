import common

def run(inputs):
    possibles = common.possibles(inputs)
    diffs = common.diffs(possibles)
    counts = common.counts(possibles)

    diffs_mask = diffs.gt(-1).all(axis=1)
    counts_mask = counts.gt(1).any(axis=1)
    
    possibles = possibles[
        diffs_mask & counts_mask
    ]
    
    return len(possibles)
        
