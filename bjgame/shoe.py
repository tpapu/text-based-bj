"""A class containing a shoe holding multiples decks and dealing from it."""

from .card import *
from random import randrange


class Shoe:
    """A card shoe used for blackjack"""

    def __init__(self, num_decks=8):
        """Initialize the shoe with the specified number of decks."""
        self.num_decks = num_decks
        self.cut_card_postion = None
        self.rebuild = True
        self._shoe = None

    def _build_shoe(self):
        """Build and shuffle the shoe."""
        assert self.rebuild
        self.rebuild = False
        self.shoe = Deck()
        for _ in range(self.num_decks - 1):
            self.shoe.merge(Deck())
        self.shoe.shuffle()
        self.shoe.cut()
        # place the cut card between 60% and 80% of the shoe
        self.cut_card_position = randrange(60, 80)

    def deal_card(self, player, ncards=1):
        """Deal a card from the shoe."""
        cards = self.shoe.deal(ncards)
        player.add_cards(cards)
        if self.cut_card_position > len(self.shoe.cards):
            self.rebuild = True
