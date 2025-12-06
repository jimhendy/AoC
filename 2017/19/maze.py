import re

import a_star


class Maze(a_star.State):
    def __init__(
        self,
        grid,
        row,
        col,
        letters=None,
        n_steps=0,
        direction=(+1, 0),
    ) -> None:
        self.grid = grid
        self.row = row
        self.col = col
        self.direction = direction
        self.letters = [] if letters is None else letters
        self.n_steps = n_steps
        self.current_character = self.get_char(self.row, self.col)
        self.is_on_letter = False
        self.test_on_letter()

    def get_char(self, r, c):
        if r < 0 or c < 0:
            return None
        if r >= len(self.grid) or c >= len(self.grid[0]):
            return None
        return self.grid[r][c]

    def test_on_letter(self):
        if self.current_character is None:
            return
        match = re.findall("^([A-Z])$", self.current_character)
        if len(match):
            self.is_on_letter = True
            self.letters.append(match[0])

    def is_valid(self):
        return self.get_char(self.row, self.col) not in [None, " "]

    def is_complete(self):
        # On letter and only one way in/out
        if not self.is_on_letter:
            return False
        n_connections = 0
        left = self.get_char(self.row, self.col - 1)
        right = self.get_char(self.row, self.col + 1)
        for h in (left, right):
            if h is None:
                continue
            if re.search(r"^([A-Z\-\+\|])$", h):
                n_connections += 1
        up = self.get_char(self.row - 1, self.col)
        down = self.get_char(self.row + 1, self.col)
        for v in (up, down):
            if v is None:
                continue
            if re.search(r"^([A-Z\|\+\-])$", v):
                n_connections += 1
        return n_connections == 1

    def all_possible_next_states(self):
        if self.current_character != "+":
            # Continue in same direction
            yield Maze(
                self.grid,
                self.row + self.direction[0],
                self.col + self.direction[1],
                self.letters,
                self.n_steps + 1,
                self.direction,
            )
        # Try going orthogonally
        elif self.direction[0]:
            # Go left & right
            for dc in (-1, 1):
                yield Maze(
                    self.grid,
                    self.row,
                    self.col + dc,
                    self.letters,
                    self.n_steps + 1,
                    (0, dc),
                )
        else:
            # Go up & down
            for dr in (-1, 1):
                yield Maze(
                    self.grid,
                    self.row + dr,
                    self.col,
                    self.letters,
                    self.n_steps + 1,
                    (dr, 0),
                )

    def __lt__(self, other):
        return self.n_steps < other.n_steps

    def __repr__(self) -> str:
        return f"{self.row}_{self.col}_{self.current_character}"
