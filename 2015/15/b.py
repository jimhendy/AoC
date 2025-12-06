import os
import re

import numpy as np


class Ingredient:
    def __init__(self, capacity, durability, flavour, texture, calories) -> None:
        self.capacity = int(capacity)
        self.durability = int(durability)
        self.flavour = int(flavour)
        self.texture = int(texture)
        self.calories = int(calories)


def possible_combinations_sum(possibles, n_nums, target, others=None):
    if others is None:
        others = []
    for p in possibles:
        if p > target:
            continue
        solution = others[:]
        solution.append(p)
        if n_nums == 1 and p == target:
            yield solution
        elif n_nums > 1:
            yield from possible_combinations_sum(
                possibles,
                n_nums - 1,
                target - p,
                solution,
            )


def run(inputs):
    num_ingredients = 100

    reg = re.compile(
        r"(\D+)\: capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)",
    )

    ings = {}
    for match in reg.findall(inputs.replace(os.linesep, "")):
        ings[match[0]] = Ingredient(match[1], match[2], match[3], match[4], match[5])

    np.tile(np.arange(0, num_ingredients + 1), len(ings)).reshape(
        -1,
        num_ingredients + 1,
    )

    best_score = 0
    for comb in possible_combinations_sum(
        np.arange(0, num_ingredients + 1),
        len(ings),
        num_ingredients,
    ):
        cal = max([0, sum([i.calories * n for i, n in zip(ings.values(), comb, strict=False)])])
        if cal != 500:
            continue

        cap = max([0, sum([i.capacity * n for i, n in zip(ings.values(), comb, strict=False)])])
        dur = max([0, sum([i.durability * n for i, n in zip(ings.values(), comb, strict=False)])])
        tex = max([0, sum([i.texture * n for i, n in zip(ings.values(), comb, strict=False)])])
        fla = max([0, sum([i.flavour * n for i, n in zip(ings.values(), comb, strict=False)])])

        score = cap * dur * tex * fla

        best_score = max(score, best_score)

    return best_score
