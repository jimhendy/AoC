import pandas as pd

def run(inputs):

    serial_number = int(inputs)

    df = pd.DataFrame(
        [
            {
                'x': x,
                'y': y
            }
            for x in range(1,301)
            for y in range(1,301)
        ]
    )
    df['rackId'] = df.x + 10
    df['power'] = df.rackId * df.y
    df['power'] += serial_number
    df['power'] *= df.rackId
    df['power'] = df.power.apply(lambda x : int(f'{x:04}'[-3]))
    df['power'] -= 5

    np_power = df.pivot_table(index='y', columns='x', values='power').values

    max_power = 0
    max_power_loc = None
    grid_size = 3

    for x in range(df.x.max()-grid_size):
        for y in range(df.y.max()-grid_size):
            power = np_power[x:x+grid_size, y:y+grid_size].sum().sum()
            if power > max_power:
                max_power = power
                max_power_loc = (x+1,y+1)

    return f'{max_power_loc[1]},{max_power_loc[0]}'