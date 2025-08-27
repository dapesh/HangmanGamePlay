import random

WORDS = [
    "python", "malaysia", "hangman",
    "developer", "keyboard", "science", "variable"
]

PHRASES = [
    "hello world", "open ai chatbot",
    "machine learning", "software engineer"
]

class HangmanGame:
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
        return " ".join(
            letter if letter in self.guessed_letters or letter == " " else "_"
            for letter in self.word
        )
    def is_word_guessed(self):
        """Check if all letters in the word have been guessed."""
        return all(letter in self.guessed_letters or letter == " " for letter in self.word)

    def process_guess(self, guess):
        if guess in self.guessed_letters:
            return "already guessed"

        self.guessed_letters.append(guess)

        if guess in self.word:
            return "win" if self.is_word_guessed() else "correct"
        else:
            self.lives -= 1
            return "lose" if self.lives == 0 else "wrong"
        
    def process_timeout(self):
        self.lives -= 1
        return "lose" if self.lives == 0 else "timeout"


