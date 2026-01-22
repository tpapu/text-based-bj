"""A suited card class"""

from collections import namedtuple
from random import shuffle

# a named tuple for cards
_Card = namedtuple("Card", ["value", "suit"])


class Card(_Card):
    """A class representing a playing card with a suit and value."""

    values = (
        ["Ace"] + [str(x) for x in range(2, 11)] + ["Jack", "Queen", "King"]
    )
    suits = "♠️ ♥️ ♦️ ♣️".split()
    ranks = list(range(1, 11)) + [10, 10, 10]
    rank_dict = dict(zip(values, ranks))

    def __str__(self):
        """String representation of the card."""
        return f"{self.value} of {self.suit}"

    def __repr__(self):
        """Official string representation of the card."""
        return f"Card(value='{self.value}', suit='{self.suit}')"

    def is_Ace(self):
        """Check if the card is an Ace."""
        return self.value == "Ace"

    def is_Ten(self):
        """Check if the card is a Ten or a face card."""
        return self.rank_dict[self.value] == 10

    def __int__(self):
        """Return the integer value of the card."""
        return self.rank_dict[self.value]


class Hand:
    """A class representing a hand of playing cards."""

    def __init__(self):
        """Initialize an empty hand."""
        self.cards = []
        self.cursor = 0

    def add_cards(self, new_cards):
        """Add cards to the hand."""
        self.cards.extend(new_cards)

    def clear(self):
        """Clear the hand of all cards."""
        self.cards.clear()

    def __str__(self):
        """String representation of the hand."""
        return ", ".join(str(card) for card in self.cards)

    def __len__(self):
        """Return the number of cards in the hand."""
        return len(self.cards)

    def __is_empty__(self):
        """Check if the hand is empty."""
        return len(self.cards) == 0

    def __str__(self):
        """String representation of the hand."""
        return ", ".join(str(card) for card in self.cards)

    def __next__(self):
        """Return the next card in the hand."""
        return self.cards.__next__()

    def __iter__(self):
        """Return an iterator over the cards in the deck."""
        return iter(self.cards)


class Deck(Hand):
    """A class representing a standard deck of 52 playing cards."""

    def __init__(self):
        """Initialize the deck with 52 cards."""
        self.cards = [
            Card(value, suit) for suit in Card.suits for value in Card.values
        ]

    def shuffle(self, n=1):
        """Shuffle the deck of cards."""
        for _ in range(n):
            shuffle(self.cards)

    def cut(self):
        """cut the deck at halfway"""
        half = len(self.cards) // 2
        self.cards = self.cards[half:] + self.cards[:half]
        top_half = self.cards[:half]
        bottom_half = self.cards[half:]
        self.cards = bottom_half + top_half

    def deal(self, ncards=1):
        """Deal a card from the deck."""
        return [self.cards.pop() for _ in range(ncards)]

    def merge(self, other_deck):
        """Merge another deck into this deck."""
        try:
            self.cards.extend(other_deck.cards)
            other_deck.cards.clear()
        except (AttributeError, TypeError) as exc:
            raise AssertionError("deck does not have any _cards.") from exc


class Blackjackhand(Hand):
    """A class representing a blackjack hand."""

    def has_ace(self):
        """Check if the hand contains an Ace."""
        return any(card.is_Ace() for card in self.cards)

    @property
    def value(self):
        """Sum cards in current hand"""
        value = sum(map(int, self.cards))
        if self.has_ace():
            if (value + 10) <= 21:
                value += 10
        return value

    def int(self):
        """Return the integer value of the hand."""
        return self.value

    def is_natblackjack(self):
        """Check if the hand is a blackjack."""
        return len(self.cards) == 2 and self.value == 21

    def is_bust(self):
        """Check if the hand is bust."""
        return self.value > 21

    def is_blackjack(self):
        """check if the hand is blackjack and not natural blackjack"""
        return self.value == 21

    def is_soft(self):
        """Check if the hand is soft (contains an Ace counted as 11)"""
        if not self.has_ace():
            return False
        value = sum(map(int, self.cards))
        return (value + 10) <= 21
