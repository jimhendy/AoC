import os
from collections import defaultdict


def run(inputs):
    allergens = {}  # Allergen to set of possible ingredients
    ingredient_counts = defaultdict(int)  # Ingredient to number of sightings

    for line in inputs.split(os.linesep):
        ingredients, contains = line.split("(")
        ingredients = set([i.strip() for i in ingredients.split()])
        contains = [c.strip() for c in contains[9:-1].split(",")]
        for c in contains:
            if not c in allergens.keys():
                allergens[c] = ingredients
            else:
                allergens[c] = allergens[c].intersection(ingredients)
        for i in ingredients:
            ingredient_counts[i] += 1

    total = 0
    for i, i_count in ingredient_counts.items():
        if any([i in v for v in allergens.values()]):
            continue
        total += i_count

    return total
