from register_code import RegisterCode
import pandas as pd


def run(inputs):
    rc = RegisterCode(inputs)
    rc()
    return pd.DataFrame(rc.history).max().max()
