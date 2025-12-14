def run(input: str) -> int:
    """Count how many regions can be successfully tiled with the given shapes."""
    total = 0

    # Parse input: shapes have "#" in them, regions are dimension specifications
    input_sections = input.strip().split("\n\n")
    for section in input_sections:
        if "#" in section:
            continue
        for region_line in section.split("\n"):
            line_parts = region_line.split(":")
            w, h = map(int, line_parts[0].split("x"))
            n_shapes = sum(map(int, line_parts[1].split()))
            total += w * h >= 9 * n_shapes

    return total
