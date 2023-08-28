import os
import re

import numpy as np
from tile import Tile


def run(inputs):
    tiles = [Tile(i) for i in inputs.split(os.linesep * 2)]

    for ti in tiles:
        for i, ei in ti.nominal_edges():
            for tj in tiles:
                if tj == ti:
                    continue
                for _, ej in tj.edges():
                    if ei == ej:
                        ti.matches.append({"MySide": i, "Them": tj})

    sorted_tiles = sorted(tiles, key=lambda x: len(x.matches))
    top_left = sorted_tiles[0]
    top_left.located = True
    # Rotate the top-left tile so it's matches are on the correct sides
    while any(m["MySide"] not in ["right", "bottom"] for m in top_left.matches):
        top_left.rotate_clockwise()

    ordered_tiles = [[top_left]]

    while any(not t.located for t in tiles):
        if len(ordered_tiles[-1]) == np.sqrt(len(tiles)):
            prev_tile = ordered_tiles[-1][0]
            prev_side = "bottom"
            this_side = "top"
            ordered_tiles.append([])
        else:
            prev_tile = ordered_tiles[-1][-1]
            prev_side = "right"
            this_side = "left"

        match = next(m for m in prev_tile.matches if m["MySide"].endswith(prev_side))
        this_tile = match["Them"]

        current_side = getattr(prev_tile, prev_side)()
        found = False
        for edge, side in this_tile.edges():
            if side == current_side:
                found = True
                break
        assert found is True

        # Must be a cleaner way to do this...
        if this_side == "top":
            if edge == "reversed_top":
                this_tile.flip_horizontal()
            elif edge.endswith("right"):
                [this_tile.rotate_clockwise() for _ in range(3)]
                if edge == "reversed_right":
                    this_tile.flip_horizontal()
            elif edge.endswith("bottom"):
                [this_tile.rotate_clockwise() for _ in range(2)]
                if edge == "bottom":
                    this_tile.flip_horizontal()
            elif edge.endswith("left"):
                this_tile.rotate_clockwise()
                if edge == "left":
                    this_tile.flip_horizontal()
        elif this_side == "left":
            if edge == "reversed_left":
                this_tile.flip_vertical()
            elif edge.endswith("top"):
                [this_tile.rotate_clockwise() for _ in range(3)]
                if edge == "top":
                    this_tile.flip_vertical()
            elif edge.endswith("right"):
                [this_tile.rotate_clockwise() for _ in range(2)]
                if edge == "right":
                    this_tile.flip_vertical()
            elif edge.endswith("bottom"):
                this_tile.rotate_clockwise()
                if edge == "reversed_bottom":
                    this_tile.flip_vertical()

        ordered_tiles[-1].append(this_tile)
        this_tile.located = True

    grid = []
    for ot_row in ordered_tiles:
        for image_rows in zip(*[t.image() for t in ot_row]):
            grid.append("".join(["".join(i) for i in image_rows]))

    sea_monster = re.compile(
        r"^(.{18})#(.)\n#(.{4})##(.{4})##(.{4})###\n(.)#(.{2})#(.{2})#(.{2})#(.{2})#(.{2})#(.{3})$",
    )
    sea_monster_hash = 15

    sm_cols = 20
    sm_rows = 3

    # Manually found the orientation of grid which gives a non-zero "total" below
    grid = grid[::-1]

    total = 0
    for start_row in range(len(grid) - sm_rows + 1):
        for start_col in range(len(grid[0]) - sm_cols + 1):
            sub_grid = os.linesep.join(
                [
                    row[start_col : start_col + sm_cols]
                    for row in grid[start_row : start_row + sm_rows]
                ],
            )
            if sea_monster.search(sub_grid):
                total += sea_monster_hash

    return "".join(grid).count("#") - total
