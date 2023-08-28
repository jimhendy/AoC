ROCK = 0
SAND = 1
FALL_FROM = 500

# Points are complex numbers
# x = real component, left negative, right positive
# y = imag component, 0 at top and increasing towards the bottom of the page


def parse_point(str_rep: str) -> complex:
    x, y = map(int, str_rep.split(","))
    return x + 1j * y


def crange(start, end):
    return range(int(min(start, end)), int(max(start, end)) + 1)


def run(inputs):
    grid: dict[complex:int] = {}
    max_y = -1

    for line in inputs.splitlines():
        points = map(parse_point, line.split("->"))
        start = next(points)
        for end in points:
            if start.real == end.real:
                for y in crange(start.imag, end.imag):
                    grid[start.real + 1j * y] = ROCK
            else:
                for x in crange(start.real, end.real):
                    grid[x + 1j * start.imag] = ROCK
            start = end
            max_y = max(max_y, start.imag, end.imag)

    starting_loc = FALL_FROM + 1j * 0
    n_sand = 0
    sand = starting_loc
    while sand.imag <= max_y:
        under = sand + 1j
        if under in grid:
            if under - 1 not in grid:
                sand = under - 1
            elif under + 1 not in grid:
                sand = under + 1
            else:
                # Settle
                grid[sand] = SAND
                sand = starting_loc
                n_sand += 1
        else:
            sand = under

    return n_sand
