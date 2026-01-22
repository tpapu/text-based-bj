"""Main game logic for Blackjack game"""

from .player import BlkJckPlayer, Dealer
from .card import Deck
from .shoe import Shoe
from .mulitplayer import Multiplayer
import pickle
import os


class BlackJackGame:
    """Main Blackjack game class that manages game flow and rules"""

    def __init__(self):
        """Initialize the blackjack game"""
        self.shoe = Shoe(num_decks=8)
        self.players = []
        self.dealer = Dealer()
        self.multiplayer = None
        self.save_file = "player_data.pkl"

    def load_player_data(self):
        """Load player data from pickle file"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "rb") as f:
                    return pickle.load(f)
            except (pickle.UnpicklingError, EOFError):
                return {}
        return {}

    def save_player_data(self):
        """Save player data to pickle file"""
        player_data = {}
        for player in self.players:
            player_data[str(player.player_id)] = {
                "name": player._name,
                "balance": player._balance,
                "player_id": player.player_id,
            }
        with open(self.save_file, "wb") as f:
            pickle.dump(player_data, f)

    def setup_players(self):
        """Set up players for the game"""
        player_data = self.load_player_data()

        while True:
            try:
                num_players = input("How many players (1-4)? ")
                num_players = int(num_players)
                if 1 <= num_players <= 4:
                    break
                else:
                    print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        for i in range(num_players):
            name = input(f"Enter name for player {i + 1}: ")

            # Check if player exists in saved data
            existing_player = None
            for player_id, data in player_data.items():
                if data["name"] == name:
                    existing_player = data
                    break

            if existing_player:
                player = BlkJckPlayer(name, existing_player["balance"])
                player._player_id = existing_player["player_id"]
                print(
                    f"Welcome back, {name}! Your balance is ${
                        existing_player['balance']:.2f}"
                )
            else:
                player = BlkJckPlayer(name, 100.00)
                print(f"Welcome, {name}! Starting balance: $100.00")

            self.players.append(player)

        self.multiplayer = Multiplayer(self.players)

    def place_bets(self):
        """Have all players place their bets"""
        print("\n" + "=" * 50)
        print("PLACING BETS")
        print("=" * 50)
        for player in self.players:
            if player._balance <= 0:
                print(f"\n{player._name} is broke!")
                answer = input(
                    f"Would you like $100 from an anonymous donor? (y/n): "
                ).lower()
                if answer == "y":
                    player._balance = 100.00
                    print(f"{player._name} received $100.00!")
                else:
                    print(f"{player._name} cannot play this round.")
                    continue

            player.wager()

    def deal_initial_cards(self):
        """Deal initial two cards to each player and dealer"""
        print("\n" + "=" * 50)
        print("DEALING CARDS")
        print("=" * 50)

        # Build shoe if needed
        if self.shoe.rebuild:
            self.shoe._build_shoe()

        # First card to each player
        for player in self.players:
            if player.current_bet > 0:
                card = self.shoe.shoe.deal(1)[0]
                player.hand.add_cards([card])
                print(f"{player._name} receives: {card}")

        # First card to dealer (face up)
        card = self.shoe.shoe.deal(1)[0]
        self.dealer.hand.add_cards([card])
        print(f"Dealer receives: {card}")

        # Second card to each player
        for player in self.players:
            if player.current_bet > 0:
                card = self.shoe.shoe.deal(1)[0]
                player.hand.add_cards([card])
                print(f"{player._name} receives: {card}")

        # Second card to dealer (face down)
        card = self.shoe.shoe.deal(1)[0]
        self.dealer.hand.add_cards([card])
        print("Dealer receives: [HIDDEN CARD]")

        # Check if we've hit the cut card
        if self.shoe.cut_card_position > len(self.shoe.shoe.cards):
            self.shoe.rebuild = True

    def player_turn(self, player):
        """Execute a single player's turn"""
        if player.current_bet <= 0:
            return

        print("\n" + "-" * 50)
        print(f"{player._name}'S TURN")
        print("-" * 50)
        print(f"Dealer showing: {self.dealer.hand.cards[0]}")
        print(player.return_status())
        print(f"Current bet: ${player.current_bet:.2f}")

        # Check for immediate blackjack
        if player.hand.value == 21:
            print(f"{player._name} has BLACKJACK!")
            return

        # Player hits or stands
        while player.hand.value < 21:

            answer = input("Do you want to hit? (y/n): ").lower()
            while answer not in ["y", "n"]:
                print("Invalid input. Please enter 'y' or 'n'.")
                answer = input("Do you want to hit? (y/n): ").lower()

            if answer == "y":
                card = self.shoe.shoe.deal(1)[0]
                player.hand.add_cards([card])
                print(f"{player._name} receives: {card}")
                print(player.return_status())

                if player.hand.value > 21:
                    print(f"{player._name} BUSTED!")
                    break
                elif player.hand.value == 21:
                    print(f"{player._name} reached 21!")
                    break
            else:
                print(f"{player._name} stands with {player.hand.value}")

                break

        # Check if we've hit the cut card
        if self.shoe.cut_card_position > len(self.shoe.shoe.cards):
            self.shoe.rebuild = True

    def dealer_turn(self):
        """Execute the dealer's turn"""
        print("\n" + "=" * 50)
        print("DEALER'S TURN")
        print("=" * 50)

        # Check if any players are still in play (not busted)
        active_players = [
            p for p in self.players if p.current_bet > 0 and p.hand.value <= 21
        ]

        if not active_players:
            print("All players busted. Dealer stands.")
            print(f"Dealer's hidden card: {self.dealer.hand.cards[1]}")
            print(self.dealer.status())

            return

        # Reveal hidden card
        print(f"Dealer reveals hidden card: {self.dealer.hand.cards[1]}")
        print(self.dealer.status())

        # Dealer hits according to rules
        while self.dealer.spite_Hit():

            card = self.shoe.shoe.deal(1)[0]
            self.dealer.hand.add_cards([card])
            print(f"Dealer receives: {card}")
            print(self.dealer.status())

            if self.dealer.hand.value > 21:
                print("Dealer BUSTED!")

                break
            elif self.dealer.hand.value >= 17:
                print(f"Dealer stands with {self.dealer.hand.value}")

                break

        # Check if we've hit the cut card
        if self.shoe.cut_card_position > len(self.shoe.shoe.cards):
            self.shoe.rebuild = True

    def determine_winners(self):
        """Determine winners and update balances"""
        print("\n" + "=" * 50)
        print("RESULTS")
        print("=" * 50)

        dealer_value = self.dealer.hand.value
        dealer_busted = dealer_value > 21

        for player in self.players:
            if player.current_bet <= 0:
                continue

            player_value = player.hand.value
            player_busted = player_value > 21

            print(f"\n{player._name}: {player_value} | Dealer: {dealer_value}")

            if player_busted:
                # Player busted - loses bet
                player._balance -= player.current_bet
                print(
                    f"{player._name} BUSTED and loses ${player.current_bet:.2f}"
                )
            elif dealer_busted:
                # Dealer busted - player wins 2-to-1
                # Player wins amount equal to their bet (net gain = bet)
                player._balance += player.current_bet
                print(f"{player._name} WINS ${player.current_bet:.2f}!")
            elif player_value > dealer_value:
                # Player has higher value - wins 2-to-1
                player._balance += player.current_bet
                print(f"{player._name} WINS ${player.current_bet:.2f}!")
            elif player_value < dealer_value:
                # Dealer has higher value - player loses
                player._balance -= player.current_bet
                print(f"{player._name} LOSES ${player.current_bet:.2f}")
            else:
                # Push - tie, no change
                print(f"{player._name} PUSHES (tie)")

            print(f"{player._name}'s new balance: ${player._balance:.2f}")

    def clear_hands(self):
        """Clear all hands for next round"""
        for player in self.players:
            player.hand.clear()
            player.current_bet = 0
        self.dealer.hand.clear()

    def play_round(self):
        """Play a single round of blackjack"""
        self.place_bets()
        self.deal_initial_cards()

        # Each player takes their turn
        for player in self.players:
            self.player_turn(player)

        # Dealer takes turn
        self.dealer_turn()

        # Determine winners and update balances
        self.determine_winners()

        # Clear hands for next round
        self.clear_hands()

    def play(self):
        """Main game loop"""
        print("=" * 50)
        print("WELCOME TO BLACKJACK!")
        print("=" * 50)

        self.setup_players()

        while True:
            self.play_round()

            # Ask if players want to continue
            print("\n" + "=" * 50)
            answer = input(
                f"{self.players[0]._name}, would you like to play again? (y/n): "
            ).lower()
            while answer not in ["y", "n"]:
                print("Invalid input. Please enter 'y' or 'n'.")
                answer = input("Would you like to play again? (y/n): ").lower()

            if answer == "n":
                break

            print("\nStarting new round...\n")

        # Save player data before exiting
        self.save_player_data()
        print("\n" + "=" * 50)
        print("Thanks for playing! Game data saved.")
        print("=" * 50)


def main():
    """Main entry point for the game"""
    game = BlackJackGame()
    game.play()


if __name__ == "__main__":
    main()
