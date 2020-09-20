class Layer:
    def __init__(self, depth, range_):
        self.depth = depth
        self.range = range_
        self.scanner_range_position = 0
        self.direction = 1

    def step(self):
        proposed_position = self.scanner_range_position + self.direction
        if 0 <= proposed_position < self.range:
            self.scanner_range_position = proposed_position
        else:
            self.direction *= -1
            self.scanner_range_position += self.direction

    def severity(self):
        return self.range * self.depth
