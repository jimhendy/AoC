import heapq

Point = tuple[int, int, int]


def run(input: str) -> int:
    distances: dict[tuple[Point, Point], int] = {}
    groups: dict[Point, int] = {}
    group_id = 0

    points: list[Point] = [
        tuple(map(int, line.split(","))) for line in input.splitlines()
    ]

    for i, p1 in enumerate(points):
        for p2 in points[i + 1 :]:
            distances[(p1, p2)] = (
                (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2
            )

    heap = [(dist, (p1, p2)) for (p1, p2), dist in distances.items()]
    heapq.heapify(heap)

    for _ in range(1_000):
        p1, p2 = heapq.heappop(heap)[1]

        g1 = groups.get(p1)
        g2 = groups.get(p2)

        if g1 is not None and g2 is not None:
            if g1 != g2:
                for p, g in groups.items():
                    if g == g2:
                        groups[p] = g1
            else:
                pass
        elif g1 is not None:
            groups[p2] = g1
        elif g2 is not None:
            groups[p1] = g2
        else:
            group = group_id
            groups[p1] = group
            groups[p2] = group
            group_id += 1

    group_id_to_size: dict[int, int] = {}
    for group in groups.values():
        if group not in group_id_to_size:
            group_id_to_size[group] = 0
        group_id_to_size[group] += 1

    total = 1
    for size in sorted(group_id_to_size.values(), reverse=True)[:3]:
        total *= size
    return total
