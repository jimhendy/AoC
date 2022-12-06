from collections import defaultdict

UNIQUE_CHARACTERS = 4


def run(inputs):
    char_counts = defaultdict(int)
    entering = 0
    while sum(map(bool, char_counts.values())) != UNIQUE_CHARACTERS:
        char_counts[inputs[entering]] += 1
        leaving = entering - UNIQUE_CHARACTERS
        if leaving >= 0:
            char_counts[inputs[leaving]] -= 1
        entering += 1
    return entering
