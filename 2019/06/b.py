import common


def run(inputs):
    orbits = common.extract_orbits(inputs)

    you = common.get_orbit_list('YOU', orbits)
    san = common.get_orbit_list('SAN', orbits)

    # Reverse the lists and find the point they diverge
    for you_i, you_o in enumerate(you[::-1]):
        if not san[-you_i-1] == you_o:
            break
        pass

    # you_i now holds the index of the divergence
    num_steps = len(you) - you_i + len(san) - you_i

    return num_steps
