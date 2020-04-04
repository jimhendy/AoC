import numpy as np

DISK_LEN = 272


def step_create_data(a):
    b = (np.flip(a) + 1) % 2
    return np.hstack([a, [0], b])


def get_checksum(a):
    if len(a) % 2 == 1:
        a = a[:-1]
    return (a.reshape(-1, 2).sum(axis=1) + 1) % 2


def run(inputs):
    data = np.array(list(map(int, inputs)))

    while len(data) < DISK_LEN:
        data = step_create_data(data)
    
    checksum = get_checksum(data[:DISK_LEN])
    
    while len(checksum) % 2 == 0:
        checksum = get_checksum(checksum)

    return ''.join(map(str,checksum))