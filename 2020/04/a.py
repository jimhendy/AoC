import os


def run(inputs):
    fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
    ignore_fields = ["cid"]

    total = 0
    data = {}
    for line in inputs.split(os.linesep):
        if not line.strip():
            if all([f in data.keys() for f in fields if f not in ignore_fields]):
                total += 1
            data = {}
            continue
        for d in line.split():
            data[d.split(":")[0].strip()] = d.split(":")[1].strip()

    if all([f in data.keys() for f in fields if f not in ignore_fields]):
        total += 1

    return total
