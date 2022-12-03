import pandas as pd
from register_code import RegisterCode


def run(inputs):
    rc = RegisterCode(inputs)
    rc()
    return pd.DataFrame(rc.history).max().max()
