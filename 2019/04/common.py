import numpy as np
import pandas as pd

def possibles(inputs):
    Min,Max = [int(i) for i in inputs.split('-')]
    possibles = pd.DataFrame([list(str(i)) for i in np.arange(Min,Max)]).astype(int)
    return possibles

def diffs(possibles):
    return possibles.diff(axis=1).fillna(0)

def counts(possibles):
    counts = {
	i : possibles.eq(i).sum(axis=1)
        for i in np.unique(
                possibles.values.ravel()
	)
    }
    return pd.concat(counts, axis=1, sort=False)
