from knot_hash import knot_hash

def kh_to_binary(kh):
    return ''.join(
        map(
            lambda x : bin(int(x, 16))[2:].zfill(4),
            kh
        )
    )

def run(inputs):
    total = 0
    for i in range(128):
        kh = knot_hash(f'{inputs}-{i}')
        bin_rep = kh_to_binary(kh)
        total += bin_rep.count('1')
    return total