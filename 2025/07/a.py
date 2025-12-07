def run(input: str) -> int:
    lines = input.splitlines()
    total = 0
    beams = [lines[0].index("S")]
    for line in lines[1:]:
        new_beams = set()
        for beam in beams:
            if line[beam] == ".":
                new_beams.add(beam)
            elif line[beam] == "^":
                new_beams.add(beam - 1)
                new_beams.add(beam + 1)
                total += 1
        beams = new_beams
    return total
