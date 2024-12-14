import os

# Below 3 functions stolen from : https://math.stackexchange.com/questions/2218763/how-to-find-lcm-of-two-numbers-when-one-starts-with-an-offset


def combine_phased_rotations(a_period, a_phase, b_period, b_phase):
    """
    Combine two phased rotations into a single phased rotation.

    Returns: combined_period, combined_phase

    The combined rotation is at its reference point if and only if both a and b
    are at their reference points.
    """
    gcd, s, t = extended_gcd(a_period, b_period)
    print(gcd, s, t)
    phase_difference = a_phase - b_phase
    pd_mult, pd_remainder = divmod(phase_difference, gcd)
    if pd_remainder:
        msg = "Rotation reference points never synchronize."
        raise ValueError(msg)

    combined_period = a_period // gcd * b_period
    combined_phase = (a_phase - s * pd_mult * a_period) % combined_period
    return combined_period, combined_phase


def arrow_alignment(red_len, green_len, advantage):
    """Where the arrows first align, where green starts shifted by advantage."""
    period, phase = combine_phased_rotations(
        red_len,
        0,
        green_len,
        -advantage % green_len,
    )
    return -phase % period


def extended_gcd(a, b):
    """
    Extended Greatest Common Divisor Algorithm.

    Returns
    -------
        gcd: The greatest common divisor of a and b.
        s, t: Coefficients such that s*a + t*b = gcd

    Reference:
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode

    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


from chinese_remainder import chinese_remainder


def run(inputs):
    inputs = inputs.split(os.linesep)
    buses = {i: int(j) for i, j in enumerate(inputs[1].split(",")) if j.isdigit()}

    return chinese_remainder([-i for i in buses], list(buses.values()))
