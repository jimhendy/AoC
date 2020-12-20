import os


class Tile:
    def __init__(self, lines):
        lines = lines.split(os.linesep)
        self.id_num = int(lines[0].split()[1].rstrip(":"))
        self.grid = [list(l) for l in lines[1:]]
        self.matches = []
        self.located = False

    def top(self):
        return "".join(self.grid[0])

    def left(self):
        return "".join([l[0] for l in self.grid])

    def right(self):
        return "".join([l[-1] for l in self.grid])

    def bottom(self):
        return "".join(self.grid[-1])

    def nominal_edges(self):
        for e in ["top", "bottom", "left", "right"]:
            yield e, getattr(self, e)()

    def reverse_edges(self):
        for e, i in self.nominal_edges():
            yield f"reversed_{e}", i[::-1]

    def edges(self):
        yield from self.nominal_edges()
        yield from self.reverse_edges()

    def rotate_clockwise(self):
        self.grid = [list(row) for row in zip(*reversed(self.grid))]
        for i, m in enumerate(self.matches):
            self.matches[i]["MySide"] = {
                "top": "right",
                "bottom": "left",
                "left": "top",
                "right": "bottom",
                "reversed_top": "reversed_right",
                "reversed_bottom": "reversed_left",
                "reversed_left": "reversed_top",
                "reversed_right": "reversed_bottom",
            }[m["MySide"]]

    def flip_vertical(self):
        self.grid = self.grid[::-1]
        for i, m in enumerate(self.matches):
            self.matches[i]["MySide"] = {
                "top": "bottom",
                "bottom": "top",
                "left": "reversed_left",
                "right": "reversed_right",
                "reversed_top": "reversed_bottom",
                "reversed_bottom": "reversed_top",
                "reversed_left": "left",
                "reversed_right": "right",
            }[m["MySide"]]

    def flip_horizontal(self):
        self.grid = [l[::-1] for l in self.grid]
        for i, m in enumerate(self.matches):
            self.matches[i]["MySide"] = {
                "top": "reversed_top",
                "bottom": "reversed_bottom",
                "left": "right",
                "right": "left",
                "reversed_top": "top",
                "reversed_bottom": "bottom",
                "reversed_left": "reversed_right",
                "reversed_right": "reversed_left",
            }[m["MySide"]]

    def grid_str(self):
        return os.linesep.join(["".join(l) for l in self.grid])

    def __repr__(self):
        return f"{self.id_num}, {len(self.matches)} matches"

    def image(self):
        return [row[1:-1] for row in self.grid[1:-1]]
