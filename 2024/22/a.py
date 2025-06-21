from dataclasses import dataclass


@dataclass
class SecretNumber:
    number: int

    def evolve(self) -> None:
        value = self.number * 64
        self.mix_n_prune(value)

        value = self.number // 32
        self.mix_n_prune(value)

        value = self.number * 2048
        self.mix_n_prune(value)

    def mix_n_prune(self, value: int) -> None:
        # Mix (bitwise XOR)
        self.number ^= value

        # Prune (Modulo 16777216)
        self.number %= 16777216


def run(inputs: str) -> int:
    total = 0
    for number in inputs.splitlines():
        secret_number = SecretNumber(int(number))
        for _ in range(2_000):
            secret_number.evolve()
        total += secret_number.number

    return total
