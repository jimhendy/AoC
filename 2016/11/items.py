class Item:
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"{type(self).__name__}_{self.name}"

    def __eq__(self, other):
        return (type(self) == type(other)) & (self.name == other.name)

    def __hash__(self):
        return hash(repr(self))


class Microchip(Item):
    pass


class Generator(Item):
    pass
