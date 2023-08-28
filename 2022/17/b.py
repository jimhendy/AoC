import itertools

import pandas as pd
from statsmodels.tsa.stattools import acf

# x = real component, right +ve
# y = imag component, up +ve

WIDTH = 7
_ROCKS = [
    [complex(0, 0), complex(1, 0), complex(2, 0), complex(3, 0)],
    [complex(1, 0), complex(0, 1), complex(1, 1), complex(2, 1), complex(1, 2)],
    [complex(0, 0), complex(1, 0), complex(2, 0), complex(2, 1), complex(2, 2)],
    [complex(0, 0), complex(0, 1), complex(0, 2), complex(0, 3)],
    [complex(0, 0), complex(0, 1), complex(1, 1), complex(1, 0)],
]
ROCKS = itertools.cycle(_ROCKS)


def run(inputs):
    jet = itertools.cycle(inputs)
    occupied = set()
    highest_rock = -1

    down_offset = complex(0, -1)
    origin_x = 2
    data = {}
    previous = 0
    N = 1_000 * len(_ROCKS)

    for rock_i in range(1, N):
        origin = complex(origin_x, highest_rock + 4)
        new_rock = [p + origin for p in next(ROCKS)]

        while True:
            # Sideways
            if next(jet) == "<":
                offset = complex(-1, 0)
                new_pos = [p + offset for p in new_rock]
                if all(p.real >= 0 for p in new_pos) and all(
                    p not in occupied for p in new_pos
                ):
                    new_rock = new_pos
            else:
                offset = complex(1, 0)
                new_pos = [p + offset for p in new_rock]
                if all(p.real < WIDTH for p in new_pos) and all(
                    p not in occupied for p in new_pos
                ):
                    new_rock = new_pos

            # Downwards
            new_pos = [p + down_offset for p in new_rock]
            if all(p.imag >= 0 for p in new_pos) and all(
                p not in occupied for p in new_pos
            ):
                new_rock = new_pos
            else:
                [occupied.add(p) for p in new_rock]
                highest_rock = max(highest_rock, *(p.imag for p in new_rock))
                break

        data[rock_i] = highest_rock - previous
        previous = highest_rock

    data = pd.Series(data)
    max_offset = None
    period = None
    max_acf = None
    bad_data = {}
    for offset in range(N // 3):
        acf_values = pd.Series(acf(data.iloc[offset:], nlags=N // 2))
        this_max = max(acf_values[1:])
        bad_data[offset] = this_max
        if max_acf is None or this_max > max_acf:
            max_acf = this_max
            period = acf_values.iloc[1:].argmax() + 1
            max_offset = offset

    # This is drity, needs fixing!
    max_offset += period  # Initial period may require settling down

    prediction_x = 1_000_000_000_000
    offset_contribution = data.iloc[:max_offset].sum()
    post_offset_x = prediction_x - max_offset
    n_full_cycles, remaining_x = divmod(post_offset_x, period)
    remaining_contribution = data.iloc[max_offset : max_offset + remaining_x].sum()
    single_period_contribution = data.iloc[max_offset : max_offset + period].sum()

    return (
        offset_contribution
        + single_period_contribution * n_full_cycles
        + remaining_contribution
        + 1
    )
