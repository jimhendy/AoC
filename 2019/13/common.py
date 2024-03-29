from enum import Enum

import pandas as pd


class Tile(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


tile_content = {
    Tile.EMPTY: " ",
    Tile.WALL: "|",
    Tile.BLOCK: "#",
    Tile.PADDLE: "_",
    Tile.BALL: "o",
}


def print_game(tiles):
    display = pd.DataFrame(tiles, columns=["x", "y", "c"])
    display["cell"] = display["c"].map(Tile)
    display = display.pivot_table(
        index="y",
        columns="x",
        values="cell",
        aggfunc="last",
    ).values

    for row in display:
        for cell in row:
            print(tile_content[cell], end="")
        print()
