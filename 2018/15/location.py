class Location:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.tup = (row, col)

    def __lt__(self, other):
        row_diff = self.row - other.row
        if row_diff == 0:
            return self.col < other.col
        else:
            return row_diff < 0

    def __gt__(self, other):
        return not self.__lt__(other)

    def __eq__(self, other):
        return self.tup == other.tup

    def __hash__(self):
        return hash(self.tup)

    def __repr__(self):
        return str(self.tup)