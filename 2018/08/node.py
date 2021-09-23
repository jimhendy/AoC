class Node:
    def __init__(self, remaining_input, parent_node=None):
        self.remaining_input = remaining_input
        self.metadata = []
        self.parent_node = parent_node
        self.n_children = remaining_input.pop(0)
        self.n_metadata = remaining_input.pop(0)
        self.children = [
            Node(remaining_input, parent_node=self) for _ in range(self.n_children)
        ]
        self.metadata = [remaining_input.pop(0) for _ in range(self.n_metadata)]

    def value(self):
        if not self.n_children:
            return sum(self.metadata)
        else:
            total = 0
            for i in self.metadata:
                try:
                    total += self.children[i - 1].value()
                except IndexError:
                    pass
            return total
