import os


def run(inputs):
    allergens = {}  # Allergen to set of possible ingredients

    for line in inputs.split(os.linesep):
        ingredients, contains = line.split("(")
        ingredients = {i.strip() for i in ingredients.split()}
        contains = [c.strip() for c in contains[9:-1].split(",")]
        for c in contains:
            if c not in allergens:
                allergens[c] = ingredients
            else:
                allergens[c] = allergens[c].intersection(ingredients)

    # Once there is one option for an allergen make the dict entry into that string
    # and remove that option from all other possibilities
    while any(isinstance(v, set) for v in allergens.values()):
        for a, i in allergens.items():
            if isinstance(i, set):
                if len(i) == 1:
                    i = i.pop()
                    allergens[a] = i
                else:
                    continue
            for aa, ii in allergens.items():
                if isinstance(ii, set) and aa != a and i in ii:
                    ii.remove(i)

    return ",".join([i[1] for i in sorted(allergens.items(), key=lambda x: x[0])])
