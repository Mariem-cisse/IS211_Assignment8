
import argparse
import random
import time


class Player:
    """Base class for players."""

    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_points(self, points):
        self.score += points


class HumanPlayer(Player):
    """Represent a human player."""

    def get_choice(self, turn_total):
        return input("Enter 'r' to roll or 'h' to hold: ").lower().strip()


class ComputerPlayer(Player):
    """Represent a computer player using the required strategy."""

    def get_choice(self, turn_total):
        threshold = min(25, 100 - self.score)

        if turn_total >= threshold:
            print(f"{self.name} chooses to hold.")
            return "h"

        print(f"{self.name} chooses to roll.")
        return "r"


class PlayerFactory:
    """Create the requested type of player."""

    @staticmethod
    def create_player(player_type, number):
        if player_type == "human":
            name = input(f"Enter the name of Player {number}: ")
            return HumanPlayer(name)

        if player_type == "computer":
            return ComputerPlayer(f"Computer {number}")

        raise ValueError("Player type must be human or computer.")


class Die:
    """Represent a six-sided die."""

    def roll(self):
        return random.randint(1, 6)


class Game:
    """Manage a two-player game of Pig."""

    def __init__(self, player1_type="human", player2_type="human"):
        self.players = [
            PlayerFactory.create_player(player1_type, 1),
            PlayerFactory.create_player(player2_type, 2),
        ]
        self.die = Die()
        self.winning_score = 100

    def play_turn(self, player, proxy=None):
        turn_total = 0

        print(f"\nIt is {player.name}'s turn!")

        while True:
            if proxy and proxy.time_is_up():
                return "timeout"

            print(f"Turn total: {turn_total}")
            print(f"Total game score: {player.score}")

            if isinstance(player, ComputerPlayer):
                choice = player.get_choice(turn_total)
            else:
                choice = player.get_choice(turn_total)

            if proxy and proxy.time_is_up():
                return "timeout"

            if choice == "r":
                roll = self.die.roll()
                print(f"{player.name} rolled a {roll}.")

                if roll == 1:
                    print("You rolled a 1. No points are added.")
                    return None

                turn_total += roll

            elif choice == "h":
                player.add_points(turn_total)
                print(f"{player.name} holds.")
                print(f"Points saved: {turn_total}")
                print(f"Total score: {player.score}")

                if player.score >= self.winning_score:
                    return "win"

                return None

            else:
                print("Invalid choice. Enter 'r' or 'h'.")

    def play(self, proxy=None):
        print("\nWelcome to the Pig Dice Game!")
        print("The first player to reach 100 points wins.")

        while True:
            if proxy and proxy.time_is_up():
                self.show_result(timed_out=True)
                return

            for player in self.players:
                if proxy and proxy.time_is_up():
                    self.show_result(timed_out=True)
                    return

                result = self.play_turn(player, proxy)

                if result == "timeout":
                    self.show_result(timed_out=True)
                    return

                if result == "win":
                    self.show_result()
                    return

    def show_result(self, timed_out=False):
        if timed_out:
            print("\nTime is up!")

        print("\nFinal Scores:")
        for player in self.players:
            print(f"{player.name}: {player.score}")

        highest_score = max(player.score for player in self.players)
        winners = [
            player for player in self.players
            if player.score == highest_score
        ]

        if len(winners) == 1:
            print(f"\n{winners[0].name} wins!")
        else:
            print("\nThe game is a tie!")


class TimedGameProxy:
    """Proxy that limits a game to one minute."""

    def __init__(self, game):
        self.game = game
        self.start_time = None
        self.time_limit = 60

    def time_is_up(self):
        return time.monotonic() - self.start_time >= self.time_limit

    def play(self):
        self.start_time = time.monotonic()
        self.game.play(proxy=self)


def main():
    parser = argparse.ArgumentParser(description="Play the Pig dice game.")

    parser.add_argument(
        "--player1",
        choices=["human", "computer"],
        default="human",
    )
    parser.add_argument(
        "--player2",
        choices=["human", "computer"],
        default="human",
    )
    parser.add_argument(
        "--timed",
        action="store_true",
        help="End the game after one minute.",
    )

    args = parser.parse_args()

    game = Game(args.player1, args.player2)

    if args.timed:
        game = TimedGameProxy(game)

    game.play()


if __name__ == "__main__":
    main()
