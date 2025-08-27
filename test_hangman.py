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

    def test_choose_word_intermediate(self):
        """Test intermediate level phrase selection"""
        random.choice = lambda x: x[-1]  # Mock to return last phrase
        phrase = self.game.choose_word("2")
        self.assertIn(phrase, PHRASES)
        self.assertEqual(phrase, PHRASES[-1])

    def test_initialize_game_resets_state(self):
        self.game.word = "old"
        self.game.lives = 1
        self.game.guessed_letters = ["x"]

        self.game.initialize_game("1")

        self.assertEqual(self.game.lives, 6)
        self.assertEqual(self.game.guessed_letters, [])
        self.assertIn(self.game.word, WORDS)

    def test_display_word(self):
        self.game.word = "hi"
        self.game.guessed_letters = ["h"]
        self.assertEqual(self.game.display_word(), "h _")

    def test_is_word_guessed_true(self):
        self.game.word = "hi"
        self.game.guessed_letters = ["h", "i"]
        self.assertTrue(self.game.is_word_guessed())


if __name__ == "__main__":
    unittest.main()
