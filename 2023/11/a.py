def run(inputs: str) -> int:
    lines = inputs.splitlines()

    galaxies = []

    empty_y = []
    empty_x = list(range(len(lines)))

    for y, line in enumerate(lines):
        if all([i == "." for i in line]):
            empty_y.append(y)
            continue
        for x, character in enumerate(line):
            if character == "#":
                location = complex(x, y)
                galaxies.append(location)

                if x in empty_x:
                    empty_x.remove(x)

    expansion = 1

    total = 0
    for i in range(len(galaxies) - 1):
        for j in range(i + 1, len(galaxies)):
            difference = galaxies[i] - galaxies[j]
            raw_distance = abs(difference.real) + abs(difference.imag)

            # Count how many empty x values are between i and j
            for x in empty_x:
                if x > min(galaxies[i].real, galaxies[j].real) and x < max(
                    galaxies[i].real, galaxies[j].real
                ):
                    raw_distance += expansion

            # Similar for empty y
            for y in empty_y:
                if y > min(galaxies[i].imag, galaxies[j].imag) and y < max(
                    galaxies[i].imag, galaxies[j].imag
                ):
                    raw_distance += expansion

            total += raw_distance

    return total
