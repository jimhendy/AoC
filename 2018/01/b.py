import os


def run(inputs):
    freq = 0
    i = 0
    freqs = list(map(int, inputs.split(os.linesep)))
    n_freqs = len(freqs)
    seen = set()

    while freq not in seen:
        delta = freqs[i % n_freqs]
        i += 1
        seen.add(freq)
        freq += delta

    return freq
