from tools.inputs import parse_grid, nb8

def run(input: str) -> int:
    points = set(parse_grid(input, whitelist="@").keys())
    total = 0
    for p in points:
        if len(points.intersection(nb8(p))) < 4:
            total += 1
    return total