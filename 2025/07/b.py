from collections import defaultdict


def run(input: str) -> int:
    lines = input.splitlines()
    beams = {lines[0].index("S"): 1}
    for line in lines[1:]:
        new_beams = defaultdict(int)
        for beam in beams:
            if line[beam] == ".":
                new_beams[beam] += beams[beam]
            elif line[beam] == "^":
                new_beams[beam - 1] += beams[beam]
                new_beams[beam + 1] += beams[beam]
        beams = new_beams
    return sum(beams.values())
