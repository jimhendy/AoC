import numpy as np


def run(input: str) -> int:
    red_tiles = [complex(*map(int, line.split(","))) for line in input.splitlines()]

    green_tiles = []
    for r1, r2 in zip(red_tiles, red_tiles[1:] + [red_tiles[0]], strict=False):
        if r1.real == r2.real:
            green_tiles.append([r1.real, r1.imag])
            green_tiles.append([r1.real, r2.imag])
            green_tiles.append([r1.real, (r1.imag + r2.imag) / 2])
        else:
            green_tiles.append([r1.real, r1.imag])
            green_tiles.append([r2.real, r1.imag])
            green_tiles.append([(r1.real + r2.real) / 2, r1.imag])

    green_tiles = np.array(green_tiles)

    max_area = 0
    for i in range(len(red_tiles)):
        p1 = red_tiles[i]
        for p2 in red_tiles[i + 1 :]:
            area = (abs(p2.real - p1.real) + 1) * (abs(p2.imag - p1.imag) + 1)

            if np.any(
                (green_tiles[:, 0] > min(p1.real, p2.real))
                & (green_tiles[:, 0] < max(p1.real, p2.real))
                & (green_tiles[:, 1] > min(p1.imag, p2.imag))
                & (green_tiles[:, 1] < max(p1.imag, p2.imag)),
            ):
                continue

            if area > max_area:
                print(f"New max area {area} found between {p1} and {p2}")
                max_area = area

    return int(max_area)
