import argparse
import glob
import os
import subprocess
import time
import re

import pandas as pd

# Time each day & part for a given year's code and print a table of the slowest parts for optimisation

parser = argparse.ArgumentParser()
parser.add_argument('year', type=int, help='Year to profile')
args = parser.parse_args()

def run_part(part_file):
    print(f'Running {part_file}')
    cmd = f'python main.py {part_file}'
    start = time.time()
    subprocess.call(cmd, shell=True)
    total = time.time() - start
    return total


def profile_year(year):
    assert os.path.isdir(str(args.year))
    parts = sorted([ f for f in glob.glob(os.path.join(str(args.year), '*', '*.py')) if re.search(os.path.join(r'\d{4}', r'\d{2}', r'[a|b].py'), f) ])
    data = { f : run_part(f) for f in parts }
    df = pd.Series(data).to_frame('Time').round(2).rename_axis('FName', axis=0).reset_index(drop=False)
    total = df.Time.sum()
    df['Part'] = df.FName.str.split(os.path.sep).str[2].str.split('.').str[0]
    df['Day'] = df.FName.str.split(os.path.sep).str[1].astype(int)
    df = df.pivot_table(index='Day', columns='Part', values='Time')
    df['Combined'] = df.sum(axis=1)
    print(df)
    print('='*30)
    print(df.sort_values('Combined', ascending=False))
    print('='*30)
    print(f'Total: {total} s')

if __name__ == '__main__':
    profile_year(args.year)

