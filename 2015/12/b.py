import json


def extract_nums(data):
    total = 0
    print(data)
    if type(data) is dict:
        if "red" in data.values():
            return 0
        else:
            for v in data.values():
                total += extract_nums(v)
    elif type(data) is list:
        for d in data:
            if type(d) is int:
                total += d
            elif type(d) is list or type(d) is dict:
                total += extract_nums(d)
    elif type(data) is int:
        total = data
    return total


def run(inputs):
    j = json.loads(inputs)

    return extract_nums(j)
