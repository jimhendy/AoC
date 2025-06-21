from collections import defaultdict
from dataclasses import dataclass
from functools import reduce

import pandas as pd


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
    prices = defaultdict(list)

    for monkey_id, number in enumerate(inputs.splitlines()):
        secret_number = SecretNumber(int(number))
        prices[monkey_id].append(secret_number.number % 10)
        for _ in range(2_000):
            secret_number.evolve()
            prices[monkey_id].append(secret_number.number % 10)

    prices = pd.DataFrame(prices)
    changes = prices.diff().dropna(how="all").astype(int).astype(str)

    window = 4
    window_changes = reduce(
        lambda x, y: y + x,
        [changes.shift(i) for i in range(window)],
    ).dropna(how="all")

    # Replace any duplicated changes (within a column) with NaN
    window_changes = window_changes.mask(window_changes.apply(pd.Series.duplicated))

    prices = prices.reindex_like(window_changes).fillna(0).astype(int).stack()
    window_changes = window_changes.stack().astype(str)

    # Group the prices by the changes and sum
    summed_prices = prices.groupby(window_changes).sum()

    return summed_prices.max()
