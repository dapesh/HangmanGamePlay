import unittest
import random
from hangman import HangmanGame, WORDS, PHRASES

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

    def test_display_word_no_guesses(self):
        """Test display with no letters guessed"""
        self.game.word = "python"
        self.assertEqual(self.game.display_word(), "_ _ _ _ _ _")

    def test_display_word_some_guesses(self):
        """Test display with some letters guessed"""
        self.game.word = "python"
        self.game.guessed_letters = ["p", "o"]
        self.assertEqual(self.game.display_word(), "p _ _ _ o _")

    def test_display_word_all_guesses(self):
        """Test display with all letters guessed"""
        self.game.word = "hi"
        self.game.guessed_letters = ["h", "i"]
        self.assertEqual(self.game.display_word(), "h i")

    def test_display_word_with_spaces(self):
        """Test display with spaces in phrase"""
        self.game.word = "hello world"
        self.game.guessed_letters = ["h", "o"]
        self.assertEqual(self.game.display_word(), "h _ _ _ o   _ o _ _ _")

    def test_is_word_guessed_true(self):
        """Test word completion detection (positive)"""
        self.game.word = "hi"
        self.game.guessed_letters = ["h", "i"]
        self.assertTrue(self.game.is_word_guessed())

    def test_is_word_guessed_false(self):
        """Test word completion detection (negative)"""
        self.game.word = "hi"
        self.game.guessed_letters = ["h"]
        self.assertFalse(self.game.is_word_guessed())

    # LIFE DEDUCTION TESTS 

    def test_life_deduction_wrong_guess(self):
        """Test that wrong guess reduces lives"""
        self.game.initialize_game("1")
        self.game.word = "python"  # Set a specific word for testing
        initial_lives = self.game.lives
        
        result = self.game.process_guess("x")  # Wrong guess
        
        self.assertEqual(result, "wrong")
        self.assertEqual(self.game.lives, initial_lives - 1)

    def test_life_deduction_timeout(self):
        """Test that timeout reduces lives"""
        self.game.initialize_game("1")
        initial_lives = self.game.lives
        
        result = self.game.process_timeout()
        
        self.assertEqual(result, "timeout")
        self.assertEqual(self.game.lives, initial_lives - 1)

    def test_no_life_deduction_correct_guess(self):
        """Test that correct guess doesn't reduce lives"""
        self.game.initialize_game("1")
        self.game.word = "python"
        initial_lives = self.game.lives
        result = self.game.process_guess("p")  # Correct guess
        self.assertEqual(result, "correct")
        self.assertEqual(self.game.lives, initial_lives)

    def test_initialize_game_resets_state(self):
        self.game.word = "old"
        self.game.lives = 1
        self.game.guessed_letters = ["x"]

        self.game.initialize_game("1")

        self.assertEqual(self.game.lives, 6)
        self.assertEqual(self.game.guessed_letters, [])
        self.assertIn(self.game.word, WORDS)


    def test_process_guess_correct(self):
        self.game.word = "hi"
        result = self.game.process_guess("h")
        self.assertEqual(result, "correct")
        self.assertIn("h", self.game.guessed_letters)

    def test_process_timeout(self):
        self.game.lives = 2
        result = self.game.process_timeout()
        self.assertEqual(result, "timeout")
        self.assertEqual(self.game.lives, 1)


if __name__ == "__main__":
    unittest.main()
