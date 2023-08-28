import os


def extract_orbits(inputs):
    lis = [i.split(")") for i in inputs.split(os.linesep)]
    return {v: k for k, v in lis}


def get_orbit_list(key, orbits):
    key_orbits = []
    prev_key = key
    while prev_key in orbits:
        prev_key = orbits[prev_key]
        key_orbits.append(prev_key)
        pass
    return key_orbits


def num_orbits(key, orbits):
    total = 0
    prev_key = key
    while prev_key in orbits:
        total += 1
        prev_key = orbits[prev_key]
        pass
    return total
