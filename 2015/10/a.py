import re


def evaluate(num):
    matches = re.findall(r"(\d)(\1*)", str(num))
    return int("".join([f"{len(m[1])+1}{m[0]}" for m in matches]))


def run(inputs):

    num = int(inputs)
    for _ in range(40):
        num = evaluate(num)
        pass
    return len(str(num))
