import hashlib


def run(inputs):

    i = 0
    n_zeros = 5
    code = ["#"] * 8
    found = []
    required_start = "0" * n_zeros

    while True:
        m = hashlib.md5()
        m.update(f"{inputs}{i}".encode("utf-8"))
        h = m.hexdigest()

        if h[:n_zeros] == required_start:
            if h[5].isdigit():
                pos = int(h[5])
                if pos < len(code) and pos not in found:
                    print(pos, h[6])
                    code[pos] = h[6]
                    found.append(pos)
                    if len(found) == len(code):
                        break
        i += 1

        pass

    return "".join(code)
