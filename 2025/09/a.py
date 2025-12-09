def run(input: str) -> int:
    tiles = [complex(*map(int, line.split(","))) for line in input.splitlines()]
    max_area = 0

    for i in range(len(tiles)):
        p1 = tiles[i]
        for p2 in tiles[i + 1 :]:
            area = (abs(p2.real - p1.real) + 1) * (abs(p2.imag - p1.imag) + 1)
            max_area = max(max_area, area)

    return int(max_area)
