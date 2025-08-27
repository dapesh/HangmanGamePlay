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
