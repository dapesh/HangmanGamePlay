
"""Hangman Game with two difficulty levels and 15-second timer per guess."""

import random
from inputimeout import inputimeout, TimeoutOccurred
# Load Dictionary files


def load_file(filename):
    """Load lines from a file and return as a list."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Warning: {filename} not found.")
        return []


WORDS = load_file("dictionary.txt")
PHRASES = load_file("phrases.txt")

if not WORDS:
    WORDS = [
        "python", "malaysia", "hangman",
        "developer", "keyboard", "science", "variable"
    ]
if not PHRASES:
    PHRASES = [
        "hello world", "open ai chatbot",
        "machine learning", "software engineer"
    ]


def choose_random_word():
    """Return a random word from dictionary.txt file"""
    return random.choice(WORDS)


def choose_random_phrase():
    """Return a random phrase from phrases.txt file"""
    return random.choice(PHRASES)


class HangmanGame:
    """Hangman game logic separate from UI."""
    def get_level_choice(self):
        """Get valid level choice from the user."""
        while True:
            print("Choose level:")
            print("1. Basic Word")
            print("2. Intermediate Phrase")
            choice = input("Enter 1 or 2: ").strip()
            if choice in ["1", "2"]:
                return choice
            print("Invalid choice. Please enter 1 or 2.")

    def handle_guess(self):
        """Handle a single guess and return the result."""
        try:
            guess = inputimeout(
                "Guess a letter (15s to answer, 'quit' to exit): ", timeout=15
            ).lower().strip()
        except TimeoutOccurred:
            print("Time's up! You lost a life")
            return self.process_timeout()

        if guess == "quit":
            return "quit"

        if len(guess) != 1 or not guess.isalpha():
            return "invalid"

        return self.process_guess(guess)

    def __init__(self):
        self.word = ""
        self.lives = 6
        self.guessed_letters = []

    def choose_word(self, level):
        """Return a random word or phrase based on level choice."""
        if level == "1":
            return choose_random_word()
        return choose_random_phrase()

    def initialize_game(self, level):
        """Initialize the game with the given level."""
        self.word = self.choose_word(level)
        self.lives = 6
        self.guessed_letters = []

    def display_word(self):
        """Return the word display with guessed letters revealed."""
        display = []
        for letter in self.word:
            if letter == " ":
                display.append(" ")
            elif letter in self.guessed_letters:
                display.append(letter)
            else:
                display.append("_")
        return " ".join(display)

    def is_word_guessed(self):
        """Check if all letters in the word have been guessed."""
        return all(
            letter in self.guessed_letters or letter == " "
            for letter in self.word
        )

    def process_guess(self, guess):
        """Process a guess and return the result."""
        if guess in self.guessed_letters:
            return "already_guessed"

        self.guessed_letters.append(guess)

        if guess in self.word:
            if self.is_word_guessed():
                return "win"
            return "correct"
        self.lives -= 1
        if self.lives == 0:
            return "lose"
        return "wrong"

    def process_timeout(self):
        """Process a timeout event."""
        self.lives -= 1
        if self.lives == 0:
            return "lose"
        return "timeout"

    def display_guessed_letters(self):
        """Return a string of all guessed letters."""
        if not self.guessed_letters:
            return ""
        return ", ".join(sorted(self.guessed_letters))


def main():
    """Main game function with UI."""
    game = HangmanGame()
    level_choice = game.get_level_choice()
    game.initialize_game(level_choice)

    print(f"\nGame started! You have {game.lives} lives.")
    print("You have 15 seconds for each guess.\n")

    while game.lives > 0 and not game.is_word_guessed():
        print(game.display_word())
        print(f"Lives left: {game.lives}\n")
        print(f"Guessed letters: {game.display_guessed_letters()}\n")

        result = game.handle_guess()

        if result == "quit":
            print(f"You quit the game. The word was: {game.word}")
            break
        if result == "invalid":
            print("Invalid input. Please enter a single letter.\n")
            continue
        if result == "already_guessed":
            print("You already guessed the letter.\n")
        elif result == "correct":
            print("Correct!\n")
        elif result == "wrong":
            print("Wrong!\n")
        elif result == "win":
            print(game.display_word())
            print(f"Congratulations! You guessed the word: {game.word}")
            break
        if result == "lose":
            break

    if game.lives == 0:
        print(game.display_word())
        print(f"Game Over! The word was: {game.word}")


if __name__ == "__main__":
    main()
