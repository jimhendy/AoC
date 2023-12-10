from collections import Counter
from dataclasses import dataclass, field
from enum import IntEnum, auto
from functools import total_ordering
from typing import ClassVar, Self


class CamelCardError(Exception):
    pass


class HandType(IntEnum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


@dataclass(frozen=True, slots=True)
@total_ordering
class Card:
    label: str
    ORDERED_LABELS: ClassVar[list[str]] = (
        ["J"] + list(map(str, range(2, 10))) + list("TQKA")
    )

    def __post_init__(self) -> None:
        if self.label not in self.ORDERED_LABELS:
            raise CamelCardError(
                f"Expected a card from {self.ORDERED_LABELS}, got {self.label}",
            )

    def __eq__(self, other: Self) -> bool:
        return self.label == other.label

    def __lt__(self, other: Self) -> bool:
        return self.ORDERED_LABELS.index(self.label) < self.ORDERED_LABELS.index(
            other.label,
        )


@dataclass(slots=True)
@total_ordering
class Hand:
    cards: list[Card]
    type_: HandType = field(init=False)

    def __post_init__(self) -> None:
        if len(self.cards) != 5:
            raise CamelCardError(
                f"Expected 5 cards, got {len(self.cards)}: {self.cards}",
            )
        self.type_ = self._extract_type()

    def _extract_type(self) -> HandType:
        possible_hands = [self.cards[:]]
        for base_card_i, base_card in enumerate(self.cards):
            if base_card.label == "J":
                possible_hands = self._replace_joker(possible_hands, base_card_i)
        return max(map(self._type_from_cards, possible_hands))

    def _replace_joker(
        self,
        possible_hands: list[list[Card]],
        base_card_i: int,
    ) -> list[list[Card]]:
        new_hands = []
        for hand in possible_hands:
            non_jokers_cards = [card.label for card in hand if card.label != "J"]
            for new_label in Card.ORDERED_LABELS:
                if new_label == "J":
                    continue

                if len(non_jokers_cards) and new_label not in non_jokers_cards:
                    continue

                new_hand = hand.copy()
                new_hand[base_card_i] = Card(new_label)
                new_hands.append(new_hand)
        return new_hands

    @staticmethod
    def _type_from_cards(cards: list[Card]) -> HandType:
        counts = Counter(cards)
        match len(counts):
            case 1:
                return HandType.FIVE_OF_A_KIND
            case 2:
                if 4 in counts.values():
                    return HandType.FOUR_OF_A_KIND
                return HandType.FULL_HOUSE
            case 3:
                if 3 in counts.values():
                    return HandType.THREE_OF_A_KIND
                return HandType.TWO_PAIR
            case 4:
                return HandType.ONE_PAIR
            case _:
                return HandType.HIGH_CARD

    def __gt__(self, other: Self) -> bool:
        if self.type_ == other.type_:
            for self_card, other_card in zip(self.cards, other.cards, strict=True):
                if self_card > other_card:
                    return True
                if other_card > self_card:
                    return False
            return False
        return self.type_ > other.type_

    def __lt__(self, other: Self) -> bool:
        if self.type_ == other.type_:
            for self_card, other_card in zip(self.cards, other.cards, strict=True):
                if self_card < other_card:
                    return True
                if other_card < self_card:
                    return False
            return False
        return self.type_ < other.type_


def run(inputs: str) -> int:
    hands = {
        int(line_sections[1]): Hand([Card(card) for card in list(line_sections[0])])
        for line_sections in (line.split() for line in inputs.splitlines())
    }

    total = 0
    for rank, (bid, hand) in enumerate(
        sorted(hands.items(), key=lambda x: x[1]),
        start=1,
    ):
        total += bid * rank

    return total
