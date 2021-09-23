import os
import pandas as pd


def run(inputs):

    s = pd.Series(inputs.split(os.linesep))

    single_match = s.str.contains("(\\D).\\1")
    pair_match = s.str.contains("(\\D{2}).*\\1")

    return len(s[single_match & pair_match])
