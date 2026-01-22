"""Creates players for the Blackjack game"""

from .card import *
from uuid import uuid4
from locale import setlocale, LC_ALL


class Player:
    """A class representing a player in the blackjack game."""

    def __init__(self, name, player_id=None):
        """Initialize a player with a name and optional ID."""
        self._name = name
        if player_id:
            self._player_id = player_id
        else:
            self._player_id = uuid4()

    @property
    def name(self):
        """Return the player's name."""
        return self._name

    @property
    def player_id(self):
        """Return the player's ID."""
        return self._player_id


class BlkJckPlayer(Player):
    """A class representing the player in the blackjack game."""

    def __init__(self, name, bankroll=100):
        """Initialize the player with a default name and optional ID."""
        super().__init__(name, None)
        self._balance = bankroll
        self.hand = Blackjackhand()
        self.current_bet = 0
        self.last_bet = 0
        try:
            setlocale(LC_ALL, "")
        except BaseException:
            pass  # If locale setting fails, just continue without it

    def is_dealer(self):
        """Check if the player is the dealer."""
        return False

    def lose_bet(self, amount):
        """Subtract the bet amount from the player's balance."""
        self._balance -= amount

    def win_bet(self, amount):
        """Add the bet amount to the player's balance."""
        self._balance += amount

    @property
    def balance(self):
        """Return the player's balance formatted as currency."""
        return f"{self._balance:,.2f}"

    @property
    def __str__(self):
        """Return the player's balance formatted as currency as a string."""
        return f"{self._balance:,.2f}"

    @balance.setter
    def balance(self, amount):
        """Set the player's balance."""
        self._balance = amount

    @property
    def balance_string(self):
        """Return the player's balance formatted as currency."""
        return f"{self._balance:,.2f}"

    @property
    def bet(self):
        """Return the player's current bet."""
        return self.current_bet

    @property
    def bet_string(self):
        """Return the player's current bet formatted as currency."""
        return f"{self.current_bet:,.2f}"

    @bet.setter
    def bet(self, gamble):
        """Set the player's current bet."""
        self.current_bet = gamble

    @property
    def prev_bet(self):
        """Return the player's previous bet."""
        return self.last_bet

    @property
    def prev_bet_string(self):
        """Return the player's previous bet formatted as currency."""
        return f"{self.last_bet:,.2f}"

    @prev_bet.setter
    def prev_bet(self, prev_gamble):
        """Set the player's previous bet."""
        self.last_bet = prev_gamble

    @property
    def hit(self):
        """Determines if the player wants to hit"""
        not_valid_input = True
        answer = None
        while not_valid_input:
            answer = input("Do you want to hit? (y/n): ").lower()
            if answer in ["y", "n"]:
                not_valid_input = False
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        return "y" == answer

    def take_card(self, card):
        """Add a card to the player's hand."""
        self.hand.add_cards([card])

    def hand_value(self):
        """Return the player's hand value."""
        return self.hand.value

    def empty_hand(self):
        """Reset player hand to empty"""
        return self.hand.clear()

    def wager(self):
        """Prompt the player to place a bet."""
        not_valid_input = True
        while not_valid_input:
            gamble = input(
                f"{self._name}, you have {self.balance_string}. How much would you like to bet? "
            )
            if gamble == "":
                print("Bet cannot be empty. Please enter a valid amount.")
                continue
            gamble = int(gamble)
            if 0 < gamble <= self._balance:
                self.bet = gamble
                self.prev_bet = gamble
                not_valid_input = False
            else:
                print(
                    f"Invalid bet amount. Please enter a value between 1 and {
                        self.balance_string}."
                )
        return True

    def has_busted(self):
        """Check if the player has busted."""
        return self.hand.is_bust()

    def has_blackjack(self):
        """ "Check if the player has blackjack."""
        return self.hand.is_blackjack()

    def return_status(self):
        """return player's status mid game."""
        value = self.hand_value()
        cards = str(self.hand)
        t = f"{self._name} has {cards} for a total of {value}."
        return t


class Dealer(BlkJckPlayer):
    """A class representing the dealer in the blackjack game."""

    def __init__(self):
        """Initialize the dealer with a default name and optional ID."""
        super().__init__("Dealer", 0)

    def is_dealer(self):
        """Check if the player is the dealer."""
        return True

    def is_AI(self):
        """Check if the dealer is an AI."""
        return True

    def spite_Hit(self):
        """Dealer will hit if less than hit on value"""
        return self.hand.value < 17 or (
            self.hand.value == 17 and self.hand.is_soft()
        )

    def will_bet(self):
        """Dealer does not bet."""
        return False

    @property
    def first_card_is_ten_or_ace(self):
        """Check if the dealer's first card is a ten-value card."""
        return self.hand.cards[0].is_Ten() or self.hand.cards[0].is_Ace()

    hit_on_17 = True

    @property
    def one_card(self):
        """Return the dealer's first card."""
        return "The dealer is showing a/an" + str(self.hand.cards[0])

    def status(self):
        """return dealer's status mid game."""
        value = self.hand_value()
        cards = str(self.hand)
        t = f"The dealer has {cards} for a total of {value}."
        return t
