import re


class Component:
    reg = re.compile(r"(\d+)\/(\d+)")

    def __init__(self, pins_str) -> None:
        match = Component.reg.findall(pins_str)
        if not len(match):
            raise f'Cannot extract component pins from supplied string "{pins_str}"'
        self.pin_a = int(match[0][0])
        self.pin_b = int(match[0][1])

    def strength(self):
        return self.pin_a + self.pin_b

    def __repr__(self) -> str:
        return f"{self.pin_a}/{self.pin_b}"

    def __contains__(self, num) -> bool:
        return num == self.pin_a or num == self.pin_b
