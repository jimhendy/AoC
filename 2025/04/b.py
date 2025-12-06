from tools.inputs import nb8, parse_grid


def run(input: str) -> int:
    points = set(parse_grid(input, whitelist="@").keys())
    total = 0
    while True:
        to_remove = set()
        for p in points:
            if len(points.intersection(nb8(p))) < 4:
                total += 1
                to_remove.add(p)
        if not to_remove:
            break
        points.difference_update(to_remove)
    return total
