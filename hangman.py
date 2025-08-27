"""Hangman Game with two difficulty levels and 15-second timer per guess."""

import random
from inputimeout import inputimeout, TimeoutOccurred
WORDS = [
    "python", "malaysia", "hangman",
    "developer", "keyboard", "science", "variable"
]

PHRASES = [
    "hello world", "open ai chatbot",
    "machine learning", "software engineer"
]

class HangmanGame:
    """Hangman game logic separate from UI."""

    def __init__(self):
        self.word = ""
        self.lives = 6
        self.guessed_letters = []

    def choose_word(self, level):
        """Return a random word or phrase based on level choice."""
        if level == "1":
            return random.choice(WORDS)
        return random.choice(PHRASES)
    
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
        return all(letter in self.guessed_letters or letter == " " for letter in self.word)

    def process_guess(self, guess):
        """Process a guess and return the result."""
        if guess in self.guessed_letters:
            return "already guessed"

        self.guessed_letters.append(guess)

        if guess in self.word:
            if self.is_word_guessed():
                return "win"
            return "correct"
        else:
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
    
def main():
    """Main game function with UI."""
    game = HangmanGame()
    
    print("Choose level:")
    print("1. Basic Word")
    print("2. Intermediate Phrase")

    # Get valid level choice
    level_choice = ""
    while level_choice not in ["1", "2"]:
        level_choice = input("Enter 1 or 2: ").strip()
        if level_choice not in ["1", "2"]:
            print("Invalid choice. Please enter 1 or 2.")

    game.initialize_game(level_choice)

    print(f"\nGame started! You have {game.lives} lives.")
    print("You have 15 seconds for each guess.\n")

    while game.lives > 0 and not game.is_word_guessed():
        print(game.display_word())
        print(f"Lives left: {game.lives}\n")

        try:
            guess = inputimeout(
                prompt="Guess a letter (15s to answer, 'quit' to exit): ",
                timeout=15
            ).lower().strip()
        except TimeoutOccurred:
            result = game.process_timeout()
            print(f"Time's up! You lost a life.\n")
            if result == "lose":
                break
            continue

        if guess == "quit":
            print(f"You quit the game. The word was: {game.word}")
            break

        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter a single letter.\n")
            continue

        result = game.process_guess(guess)
        
        if result == "already guessed":
            print("You already guessed that letter.\n")
        elif result == "correct":
            print("Correct!\n")
        elif result == "wrong":
            print("Wrong!\n")
        elif result == "win":
            print(game.display_word())
            print(f"Congratulations! You guessed the word: {game.word}")
            break
        elif result == "lose":
            break

    if game.lives == 0:
        print(game.display_word())
        print(f"Game Over! The word was: {game.word}")

    
if __name__ == "__main__":
        main()