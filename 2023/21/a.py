from tools.inputs import parse_grid, nb4
from itertools import chain

def run(inputs: str) -> int:
    grid = parse_grid(inputs, ignore_chars="#")
    plot_locations = set(grid)

    current_locations = {next(k for k, v in grid.items() if v == "S")}
    
    for _ in range(64):
        current_locations = set(
            chain.from_iterable(nb4(location) for location in current_locations)
        ) & plot_locations

    return len(current_locations)

