import pandas as pd
import os

def run(inputs):
    coords = pd.DataFrame(
        [
            {
                'x':int(i.split(',')[0]), 
                'y':int(i.split(',')[1])
            }
            for i in inputs.split(os.linesep)
        ]
    )

    max_coord = coords.max(axis=0)

    space = pd.DataFrame(
        [
            {
                'x': x,
                'y': y
            }
            for x in range(-1, max_coord.x + 2)
            for y in range(-1, max_coord.y + 2)
        ] 
    )
    
    distance_cols = []
    for i in range(len(coords)):
        col = f'Distance_{i}'
        distance_cols.append(col)
        space[col] = abs(space.x - coords.iloc[i].x) + abs(space.y - coords.iloc[i].y)

    space['MinimumForward'] = space[distance_cols].idxmin(axis=1)
    space['MinimumBackward'] = space[reversed(distance_cols)].idxmin(axis=1)

    space.loc[ space.MinimumForward.eq(space.MinimumBackward), 'Minimum'] = space.MinimumForward
    space.Minimum.fillna('.', inplace=True)

    outer_mask = space.x.eq(-1) | space.y.eq(-1) | space.x.eq(max_coord.x+1) | space.y.eq(max_coord.y+1)

    outer_space = space[outer_mask]
    inner_space = space[~outer_mask]

    ignore_distances = outer_space.Minimum.unique()

    valid_inner = inner_space[~inner_space.Minimum.isin(ignore_distances)]

    counts = valid_inner.Minimum.value_counts()

    return counts.max()