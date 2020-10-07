import os
import numpy as np
import numba

@numba.njit
def int_to_binary(num, width=16):
    binary = np.zeros(width, dtype=np.int8)
    if num != 0:
        i = 0
        while num > 0 and i < width:
            if num % 2:
                binary[i] = 1
            num = num // 2
            i += 1
    return binary[::-1]

@numba.njit
def do(start_a, start_b, factor_a, factor_b, mod, n_repeats):
    matches = 0
    val_a = start_a
    val_b = start_b
    for i in range(n_repeats):

        if not i % 100_000:
            print(i)

        val_a = (val_a * factor_a) % mod
        val_b = (val_b * factor_b) % mod

        while val_a % 4:
            val_a = (val_a * factor_a) % mod

        while val_b % 8:
            val_b = (val_b * factor_b) % mod

        bin_a = int_to_binary(val_a)
        bin_b = int_to_binary(val_b)

        if np.array_equal(bin_a, bin_b):
            matches += 1
        
    return matches

def run(inputs):
    starting_values = [
        int(i.split()[-1])
        for i in inputs.split(os.linesep)
    ]
    return do(
        starting_values[0], starting_values[1],
        16807, 48271,
        2147483647,
        5_000_000
    )