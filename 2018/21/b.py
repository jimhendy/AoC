def func(r1, r3):
    return (((r3 + (r1 & 255)) & 16777215) * 65899) & 16777215


def run(inputs):
    r3 = 0
    seen = set()
    prev_r3 = None
    while True:

        r1 = r3 | 65536
        r3 = 9450265

        r3 = func(r1, r3)

        while 256 <= r1:
            r1 = r1 // 256
            r3 = func(r1, r3)

        if r3 in seen:
            break

        seen.add(r3)
        prev_r3 = r3

    return prev_r3
