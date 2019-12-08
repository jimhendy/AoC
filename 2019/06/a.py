import common


def run(inputs):
    orbits = common.extract_orbits(inputs)
    total_orbits = sum([
        common.num_orbits(p, orbits)
        for p in orbits.keys()
    ])
    return total_orbits
