import common


def run(inputs):
    possibles = common.possibles(inputs)
    diffs = common.diffs(possibles)
    counts = common.counts(possibles)

    # Ensure all consecutive values increase
    diffs_mask = diffs.gt(-1).all(axis=1)
    # Ensure one value is repeated only twice
    # As all values increase this is enough
    double_mask = counts.eq(2).any(axis=1)

    possibles = possibles[
        diffs_mask & double_mask
    ]

    return len(possibles)
