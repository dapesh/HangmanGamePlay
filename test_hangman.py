import unittest
from hangman import HangmanGame, WORDS, PHRASES
import random

class TestHangman(unittest.TestCase):
    def setUp(self):
        self.game = HangmanGame()

    def test_choose_word_basic(self):
        """Test basic level word selection"""
        random.choice = lambda x: x[0]  # return first word
        word = self.game.choose_word("1")
        self.assertIn(word, WORDS)
        self.assertEqual(word, WORDS[0])
if __name__ == "__main__":
    unittest.main()
