import unittest
import random
from hangman import HangmanGame, WORDS, PHRASES

class TestHangman(unittest.TestCase):
    def setUp(self):
        self.game = HangmanGame()
    # Requirement 1: Two level tests
    def test_choose_word_basic(self):
        """Test basic level word selection"""
        random.choice = lambda x: x[0]
        word = self.game.choose_word("1")
        self.assertIn(word, WORDS)
        self.assertEqual(word, WORDS[0])

    def test_choose_word_intermediate(self):
        """Test intermediate level phrase selection"""
        random.choice = lambda x: x[-1]
        phrase = self.game.choose_word("2")
        self.assertIn(phrase, PHRASES)
        self.assertEqual(phrase, PHRASES[-1])
    
    #Requirement 2: Words come from valid dictionaries
    def test_initialize_game_valid_words(self):
        """Words come from valid dictionaries"""
        self.game.initialize_game("1")
        self.assertIn(self.game.word, WORDS)
    # Requirement 3: Underscores for missing letters
    def test_display_word_no_guesses(self):
        """Test display with no letters guessed"""
        self.game.word = "python"
        self.assertEqual(self.game.display_word(), "_ _ _ _ _ _")
    
    # Requirement 4: 15-second timer with life deduction
    def test_life_deduction_timeout(self):
        """Requirement 4: Timeout reduces lives"""
        initial_lives = self.game.lives
        result = self.game.process_timeout()
        self.assertEqual(result, "timeout")
        self.assertEqual(self.game.lives, initial_lives - 1)

    # Requirement 5: Correct guess reveals letters    
    def test_display_word_some_guesses(self):
        """Test display with some letters guessed"""
        self.game.word = "python"
        self.game.guessed_letters = ["p", "o"]
        self.assertEqual(self.game.display_word(), "p _ _ _ o _")

    # Requirement 6: Wrong guess deducts life
    def test_life_deduction_wrong_guess(self):
        """Test that wrong guess reduces lives"""
        self.game.initialize_game("1")
        self.game.word = "python"  
        initial_lives = self.game.lives
        
        result = self.game.process_guess("x")  # Wrong guess
        
        self.assertEqual(result, "wrong")
        self.assertEqual(self.game.lives, initial_lives - 1)
    
    # Requirement 7: Win before lives reach zero
    def test_win_condition(self):
        """Test that correct final guess wins game"""
        self.game.initialize_game("1")
        self.game.word = "hi"
        self.game.guessed_letters = ["h"]
        
        result = self.game.process_guess("i")  # Final correct guess
        
        self.assertEqual(result, "win")
        self.assertTrue(self.game.is_word_guessed())

    # Requirement 8: Game continues until quit or loss
    def test_game_over_wrong_guess(self):
        """Test that wrong guess on last life ends game"""
        self.game.initialize_game("1")
        self.game.word = "python"
        self.game.lives = 1  # Set to last life
        
        result = self.game.process_guess("x")  # Wrong guess
        
        self.assertEqual(result, "lose")
        self.assertEqual(self.game.lives, 0)

if __name__ == "__main__":
    unittest.main()
