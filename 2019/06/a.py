import common


def run(inputs):
    orbits = common.extract_orbits(inputs)
    return sum([common.num_orbits(p, orbits) for p in orbits])
