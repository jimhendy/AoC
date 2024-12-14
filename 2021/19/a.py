import os

Beacon = tuple[int, int, int]


class Scanner:
    _orientation_lambdas = [
        lambda x, y, z: (x, y, z),
        lambda x, y, z: (x, z, -y),
        lambda x, y, z: (x, -y, -z),
        lambda x, y, z: (x, -z, y),
        lambda x, y, z: (-x, -y, z),
        lambda x, y, z: (-x, z, y),
        lambda x, y, z: (-x, y, -z),
        lambda x, y, z: (-x, -z, -y),
        lambda x, y, z: (-y, x, z),
        lambda x, y, z: (-z, x, -y),
        lambda x, y, z: (y, x, -z),
        lambda x, y, z: (z, x, y),
        lambda x, y, z: (y, -x, z),
        lambda x, y, z: (z, -x, -y),
        lambda x, y, z: (-y, -x, -z),
        lambda x, y, z: (-z, -x, y),
        lambda x, y, z: (z, -y, x),
        lambda x, y, z: (-y, -z, x),
        lambda x, y, z: (-z, y, x),
        lambda x, y, z: (y, z, x),
        lambda x, y, z: (z, y, -x),
        lambda x, y, z: (y, -z, -x),
        lambda x, y, z: (-z, -y, -x),
        lambda x, y, z: (-y, z, -x),
    ]

    def __init__(self, beacons) -> None:
        self.beacons = set(beacons)
        self.scanner_locs = [(0, 0, 0)]

    def extend(
        self,
        new_scanner: "Scanner",
        new_becons: set[Beacon],
        new_scanner_pos: tuple[int, int, int],
    ):
        [self.beacons.add(b) for b in new_becons]
        for c in new_scanner.scanner_locs:
            self.scanner_locs.append(
                tuple([i + j for i, j in zip(c, new_scanner_pos, strict=False)])
            )

    def orientations(self):
        for o in self._orientation_lambdas:
            yield [o(*b) for b in self.beacons]


def compare(scanner_1, scanner_2):
    for beacons_2 in scanner_2.orientations():
        for b1 in scanner_1.beacons:
            for b2 in beacons_2:
                offset = [i - j for i, j in zip(b1, b2, strict=False)]

                beacons_2_in_1_coords = {
                    tuple([i + j for i, j in zip(bb2, offset, strict=False)])
                    for bb2 in beacons_2
                }
                overlap = beacons_2_in_1_coords.intersection(scanner_1.beacons)
                if len(overlap) >= 12:
                    scanner_1.extend(scanner_2, beacons_2_in_1_coords, offset)
                    return True

    return False


def run(inputs):
    scanners = []
    beacons = []
    for line in inputs.split(os.linesep):
        if "scanner" in line:
            continue
        if not line:
            scanners.append(Scanner(beacons))
            beacons = []
        else:
            beacons.append(tuple(map(int, line.split(","))))
    if beacons:
        scanners.append(Scanner(beacons))

    while len(scanners) > 1:
        to_remove = []

        for i, s1 in enumerate(scanners):
            for j, s2 in enumerate(scanners):
                if j in to_remove:
                    continue
                if i == j:
                    continue
                result = compare(s1, s2)
                if result:
                    to_remove.append(j)
                    print(
                        f"Combining scanner {j} into {i}, {len(scanners)-len(to_remove)} scanners left",
                    )

                else:
                    print(f"Not combining {j} into {i}")
            if len(to_remove):
                break

        if not to_remove:
            msg = "Should not be here, nothing to remove"
            raise RuntimeError(msg)

        for i, r in enumerate(to_remove):
            del scanners[r - i]

    return len(scanners[0].beacons)
