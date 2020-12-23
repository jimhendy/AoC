import tqdm


def play_round(cups, current, max_cup):
    next_three = [
        cups[current],
        cups[cups[current]],
        cups[cups[cups[current]]],
    ]

    destination = current - 1 or max_cup
    while destination in next_three:
        destination = destination - 1 or max_cup

    # Remove the 3 picked up cups
    cups[current] = cups[next_three[2]]

    # Insert the 3 cups to the right of destination
    cups[next_three[2]] = cups[destination]
    cups[next_three[1]] = next_three[2]
    cups[next_three[0]] = next_three[1]
    cups[destination] = next_three[0]

    return cups[current]


def run(inputs):
    max_cup = 1_000_000
    labels = list(map(int, list(inputs)))
    labels += list(range(max(labels) + 1, max_cup + 1))

    # Key is cup, value is cup to the right
    cups = {i: j for i, j in zip(labels[:-1], labels[1:])}
    cups[labels[-1]] = labels[0]

    current = labels[0]
    for _ in tqdm.tqdm(range(10_000_000)):
        current = play_round(cups, current, max_cup)

    return cups[1] * cups[cups[1]]
