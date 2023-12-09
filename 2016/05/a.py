import hashlib


def run(inputs):
    i = 0
    n_zeros = 5
    code = []
    required_start = "0" * n_zeros

    while True:
        m = hashlib.md5()
        m.update(f"{inputs}{i}".encode())
        h = m.hexdigest()

        if h[:n_zeros] == required_start:
            code.append(h[5])

        i += 1
        if len(code) == 8:
            break

    return "".join(code)
