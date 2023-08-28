import hashlib


def run(inputs):
    i = 0
    n_zeros = 6
    while True:
        m = hashlib.md5()
        m.update(f"{inputs}{i}".encode())
        h = m.hexdigest()

        if h[:n_zeros] == ("0" * n_zeros):
            return i

        i += 1
        pass

    pass
    return None
