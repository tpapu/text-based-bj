"""Creates a round that iterates through multiple players"""


class Multiplayer:
    """Iterates through each player to demonstrate rounds"""

    def __init__(self, players):
        """Initialize the multiplayer round with a list of players."""
        self.players = players
        self.current_player_index = 0

    def stop(self):
        """Stop the multiplayer round."""
        self.stop = True

    def next_player(self):
        """Move to the next player in the list."""
        if self.stop:
            raise StopIteration
        if not self.players:
            return None
        self.current_player_index = (self.current_player_index + 1) % len(
            self.players
        )
        return self.current_player()

    def current_player(self):
        """Return the current player."""
        if not self.players:
            return None
        return self.players[self.current_player_index]
