import re


class Component:

    reg = re.compile(r"(\d+)\/(\d+)")

    def __init__(self, pins_str):
        match = Component.reg.findall(pins_str)
        if not len(match):
            raise f'Cannot extract component pins from supplied string "{pins_str}"'
        else:
            self.pin_a = int(match[0][0])
            self.pin_b = int(match[0][1])

    def strength(self):
        return self.pin_a + self.pin_b

    def __repr__(self):
        return f"{self.pin_a}/{self.pin_b}"

    def __contains__(self, num):
        return num == self.pin_a or num == self.pin_b
