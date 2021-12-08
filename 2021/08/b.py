import os


class Display:
    def __init__(self, info):
        self.info = info
        self.wires = [set(i) for i in self.info.split("|")[0].split()]
        self.outputs = ["".join(sorted(i)) for i in self.info.split("|")[1].split()]
        self.numbers = self._extract_numbers()

    def decode(self):
        """ Return the unscrambled 4 digit number """
        return int("".join([self.numbers[n] for n in self.outputs]))

    def _get_wire_by_bits(self, bits):
        """
        Find a scrambled wire by the number of bits turned on
        """
        possibles = [w for w in self.wires if len(w) == bits]
        assert len(possibles) == 1
        return possibles[0]

    def _find_from_nearly(self, nearly):
        """
        Find a scrambled wire which has one extra bit as compared to ``nearly``.
        Also return the extra letter.
        """
        possibles = [
            w for w in self.wires if len(w - nearly) == 1 and len(w) == len(nearly) + 1
        ]
        assert len(possibles) == 1
        found_number = possibles[0]
        extra_letter = found_number - nearly
        return found_number, extra_letter

    def _extract_numbers(self):
        numbers = {}  # real number to mixed up wires
        letters = {}  # real letter to mixed up letter
        numbers[1] = self._get_wire_by_bits(2)
        numbers[7] = self._get_wire_by_bits(3)
        numbers[4] = self._get_wire_by_bits(4)
        numbers[8] = self._get_wire_by_bits(7)
        letters["a"] = numbers[7] - numbers[1]
        numbers[9], letters["g"] = self._find_from_nearly(
            numbers[1] | numbers[4] | numbers[7]
        )
        letters["e"] = numbers[8] - numbers[9]
        numbers[3], letters["d"] = self._find_from_nearly(
            numbers[1] | letters["g"] | letters["a"]
        )
        letters["b"] = numbers[4] - numbers[1] - letters["d"]
        numbers[5], letters["f"] = self._find_from_nearly(
            letters["a"] | letters["b"] | letters["d"] | letters["g"]
        )
        letters["c"] = numbers[1] - letters["f"]
        numbers[2] = numbers[3] - letters["f"] | letters["e"]
        numbers[6] = numbers[8] - letters["c"]
        numbers[0] = numbers[8] - letters["d"]

        mapping = {"".join(sorted(list(s))): str(n) for n, s in numbers.items()}
        return mapping


def run(inputs):
    total = 0
    for line in inputs.split(os.linesep):
        d = Display(line)
        total += d.decode()
    return total