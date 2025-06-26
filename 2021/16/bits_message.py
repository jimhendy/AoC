from collections import deque

from packets import Literal, Operator, Packet

from tools.number_conversion import binary_to_decimal, hex_to_binary


class BitsMessage:
    def __init__(self, hex_message: str) -> None:
        """Construct a BitsMessage.

        :param hex_message: The input hex string to decode.
        """
        self.hex_message = hex_message
        self.queue = deque(
            [j for i in list(self.hex_message) for j in hex_to_binary(i)],
        )
        self.packets = []
        self.version_total = 0
        self.pops = 0

    def extract_n_binary(self, n: int) -> list[int]:
        """Pop (from the left) ``n`` characters from the ``queue`` of binary bits.

        :param n: How many bits to return.
        :return: A list of ``n`` binary bits as single character ``str``s.
        """
        self.pops += n
        return [self.queue.popleft() for _ in range(n)]

    def extract_n_decimal(self, n: int) -> int:
        """Pop (from the left) ``n`` characters from the ``queue`` and return as a decimal number.

        :param n: How many bits to pop and convert.
        :retrun: Decimal representation of the ``n`` bit binary number.
        """
        return binary_to_decimal(self.extract_n_binary(n))

    def extract_literal_binary(self) -> list[str]:
        """Extract the literal number from the left of the ``queue`` and return as a list of binary bits.

        :return: List of single ``str`` characters of the literal.
        """
        bits = []
        while self.extract_n_decimal(1):
            bits.extend(self.extract_n_binary(4))
        bits.extend(self.extract_n_binary(4))
        return bits

    def extract_leading_packet(self) -> Packet:
        """Extract the leading (left) packet from the ``queue`` and return.

        :return: Packet subclass exrtracted from the ``queue``.
        """
        version = self.extract_n_decimal(3)
        self.version_total += version
        type_id = self.extract_n_decimal(3)

        if type_id == 4:
            return Literal(version=version, binary=self.extract_literal_binary())
        length_type_id = self.extract_n_decimal(1)
        if length_type_id == 0:
            # Next 15 bits represent total length in bits of sub-packets
            bit_lenth_of_subpackets = self.extract_n_decimal(15)
            analysed_bits = 0
            subpackets = []
            while analysed_bits != bit_lenth_of_subpackets:
                start_pops = self.pops
                literal = self.extract_leading_packet()
                analysed_bits += self.pops - start_pops
                subpackets.append(literal)
            return Operator(version=version, type_id=type_id, subpackets=subpackets)
        if length_type_id == 1:
            # Next 11 bits are number of subpackets
            n_subpackets = self.extract_n_decimal(11)
            subpackets = [self.extract_leading_packet() for _ in range(n_subpackets)]
            return Operator(version=version, type_id=type_id, subpackets=subpackets)
        msg = f"length_type_id {length_type_id} unknown"
        raise NotImplementedError(msg)
