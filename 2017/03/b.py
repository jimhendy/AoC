from collections import defaultdict


def run(inputs):

    target = int(inputs)

    data = defaultdict(int)
    data[(0, 0)] = 1
    current_coord = (0, 0)
    while True:
        next_coord = get_next_coord(current_coord)
        next_value = get_value(data, next_coord)
        if next_value > target:
            return next_value
        data[next_coord] = next_value
        current_coord = next_coord


def get_value(data, coord):
    total = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            total += data[(coord[0] + dx, coord[1] + dy)]
    return total


def get_next_coord(current_coord):

    if all([i >= 0 for i in current_coord]) and current_coord[0] == current_coord[1]:
        # Next row
        return (current_coord[0] + 1, current_coord[1])
    elif (
        current_coord[0] > 0
        and current_coord[1] > -current_coord[0]
        and current_coord[1] <= current_coord[0]
    ):
        # Move up
        return (current_coord[0], current_coord[1] - 1)
    elif current_coord[1] < 0 and current_coord[0] > current_coord[1]:
        # Move left
        return (current_coord[0] - 1, current_coord[1])
    elif current_coord[0] < 0 and current_coord[1] < -current_coord[0]:
        # Move down
        return (current_coord[0], current_coord[1] + 1)
    elif current_coord[1] > 0 and current_coord[0] < current_coord[1]:
        # Move right
        return (current_coord[0] + 1, current_coord[1])
    else:
        raise RuntimeError
