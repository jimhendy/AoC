import os


def run(inputs):
    ranges = (list(map(int, i.split("-"))) for i in inputs.split(os.linesep))
    ranges = sorted(ranges, key=lambda x: x[0])
    min_ip = 0
    for r in ranges:
        if r[0] <= min_ip:
            min_ip = max(r[1] + 1, min_ip)
        else:
            return min_ip
