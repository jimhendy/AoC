import re

import pandas as pd


def run(inputs):
    reg = re.compile(
        r"\/dev\/grid\/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)\%"
    )
    data = []
    for m in reg.findall(inputs):
        data.append(
            {
                "x": int(m[0]),
                "y": int(m[1]),
                "size": int(m[2]),
                "used": int(m[3]),
                "avail": int(m[4]),
                "use": int(m[5]),
            }
        )
    df = pd.DataFrame(data)
    total = 0
    for i, u in df.used.iteritems():
        if u == 0:
            continue
        total += len(df[(df.index != i) & df.avail.gt(u)])

    return total
