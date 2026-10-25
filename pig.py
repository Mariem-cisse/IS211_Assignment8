import random

random.seed(0)

class Player:
    """Represent a human player."""

    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_points(self, points):
        self.score += points


class Die:
    """Represent a six-sided die."""

    def roll(self):
        return random.randint(1, 6)


class PigGame:
    """Manage a two-player game of Pig."""

    def __init__(self):
        self.players = [
            Player(input("Enter the name of Player 1: ")),
            Player(input("Enter the name of Player 2: "))
        ]
        self.die = Die()
        self.winning_score = 100

    def play_turn(self, player):
        turn_total = 0
        last_roll = None

        print(f"\nIt is {player.name}'s turn!")

        while True:
            if last_roll is None:
                print("Last roll: None yet")
            else:
                print(f"Last roll: {last_roll}")

            print(f"Turn total: {turn_total}")
            print(f"Total game score: {player.score}")

            choice = input("Enter 'r' to roll or 'h' to hold: ")
            choice = choice.lower().strip()

            if choice == "r":
                last_roll = self.die.roll()
                print(f"{player.name} rolled a {last_roll}.")

                if last_roll == 1:
                    print("You rolled a 1. No points are added.")
                    print(f"{player.name}'s turn is over.")
                    return False

                turn_total += last_roll

            elif choice == "h":
                player.add_points(turn_total)
                print(f"{player.name} holds.")
                print(f"Points saved: {turn_total}")
                print(f"Total score: {player.score}")

                if player.score >= self.winning_score:
                    return True

                return False

            else:
                print("Invalid choice. Please enter 'r' or 'h'.")

    def play(self):
        print("\nWelcome to the Pig Dice Game!")
        print("The first player to reach 100 points wins.")

        while True:
            for player in self.players:
                game_over = self.play_turn(player)

                if game_over:
                    print(f"\nCongratulations, {player.name}! You win!")
                    print("\nFinal Scores:")

                    for current_player in self.players:
                        print(
                            f"{current_player.name}: "
                            f"{current_player.score}"
                        )

                    return


def main():
    game = PigGame()
    game.play()


if __name__ == "__main__":
    main()
