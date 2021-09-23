import os
import pandas as pd


def run(inputs):

    df = pd.DataFrame([list(i) for i in inputs.split(os.linesep)])

    message = []
    for c in df.columns:
        message.append(df[c].value_counts().index[0])

    return "".join(message)
