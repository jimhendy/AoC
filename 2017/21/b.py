import os
import numpy as np
from functools import lru_cache

CACHE = {}


def extract_matrix(string):
    data = string.split("/")
    return np.array([list(d) for d in data])


def extract_rules(inputs):
    rules = []
    for rule in inputs.split(os.linesep):
        i = extract_matrix(rule.split("=>")[0].strip())
        o = extract_matrix(rule.split("=>")[1].strip())
        rules.append((i, o))
    return rules


def find_possible_matches(matrix):
    return [
        matrix,
        np.flip(matrix, axis=0),
        np.flip(matrix, axis=1),
        np.rot90(matrix),
        np.rot90(np.rot90(matrix)),
        np.rot90(np.rot90(np.rot90(matrix))),
        np.flip(np.rot90(matrix), axis=1),
        np.flip(np.rot90(matrix), axis=0),
    ]


def enhance_sub_image(sub_image, rules):
    global CACHE
    image_hash = hash(sub_image.tostring())
    if image_hash in CACHE.keys():
        return CACHE[image_hash]
    for rule in rules:
        rule_i = rule[0]
        if any([np.array_equal(sub_image, m) for m in find_possible_matches(rule_i)]):
            CACHE[image_hash] = rule[1]
            return rule[1]
    raise Exception(f'Could not find match for sub-image "{sub_image}"')


def enhance(image, rules):
    size = image.shape[0]
    break_size = 2 if not size % 2 else 3
    rows = []
    for y_start in range(0, size, break_size):
        this_row = []
        for x_start in range(0, size, break_size):
            sub_image = image[
                y_start : y_start + break_size, x_start : x_start + break_size
            ]
            this_row.append(enhance_sub_image(sub_image, rules))
        rows.append(np.hstack(this_row))
    return np.vstack(rows)


def run(inputs):
    rules = extract_rules(inputs)
    image = np.array([[".", "#", "."], [".", ".", "#"], ["#", "#", "#"]])

    for i in range(18):
        print(i)
        image = enhance(image, rules)

    return len(np.argwhere(image == "#"))
