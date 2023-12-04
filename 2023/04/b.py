from collections import defaultdict

# Start with 1 copy of each card
CARD_COUNTS = defaultdict(lambda: 1)


def run(inputs: str) -> int:
    total = 0

    for card_number, line in enumerate(inputs.splitlines(), start=1):
        winning_numbers, numbers_you_have = line.split(":")[1].split("|")
        len_intersection = len(
            set(map(int, winning_numbers.split())).intersection(
                map(int, numbers_you_have.split()),
            ),
        )

        copies_of_this_card = CARD_COUNTS[card_number]
        total += copies_of_this_card

        for card_offset in range(len_intersection):
            next_card = card_number + (card_offset + 1)
            CARD_COUNTS[next_card] += copies_of_this_card

    return total
