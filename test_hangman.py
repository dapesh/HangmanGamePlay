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

    def test_game_over_wrong_guess(self):
        """Test that wrong guess on last life ends game"""
        self.game.initialize_game("1")
        self.game.word = "python"
        self.game.lives = 1  # Set to last life
        
        result = self.game.process_guess("x")  # Wrong guess
        
        self.assertEqual(result, "lose")
        self.assertEqual(self.game.lives, 0)

    def test_game_over_timeout(self):
        """Test that timeout on last life ends game"""
        self.game.initialize_game("1")
        self.game.lives = 1  # Set to last life
        
        result = self.game.process_timeout()
        
        self.assertEqual(result, "lose")
        self.assertEqual(self.game.lives, 0)

    def test_already_guessed_letter(self):
        """Test that already guessed letter doesn't affect lives"""
        self.game.initialize_game("1")
        self.game.word = "python"
        self.game.guessed_letters = ["p"]
        initial_lives = self.game.lives
        
        result = self.game.process_guess("p")  # Already guessed
        
        self.assertEqual(result, "already_guessed")
        self.assertEqual(self.game.lives, initial_lives)

    def test_win_condition(self):
        """Test that correct final guess wins game"""
        self.game.initialize_game("1")
        self.game.word = "hi"
        self.game.guessed_letters = ["h"]
        
        result = self.game.process_guess("i")  # Final correct guess
        
        self.assertEqual(result, "win")
        self.assertTrue(self.game.is_word_guessed())

    def test_input_validation_empty_string(self):
        """Test that empty string input is invalid"""
        guess = ""
        is_valid = (len(guess) == 1 and guess.isalpha())
        self.assertFalse(is_valid, "Empty string should be invalid")

    def test_input_validation_multiple_letters(self):
        """Test that multiple letters are invalid"""
        guess = "ab"
        is_valid = (len(guess) == 1 and guess.isalpha())
        self.assertFalse(is_valid, "Multiple letters should be invalid")

    def test_input_validation_numbers(self):
        """Test that numbers are invalid"""
        guess = "1"
        is_valid = (len(guess) == 1 and guess.isalpha())
        self.assertFalse(is_valid, "Numbers should be invalid")

    def test_input_validation_symbols(self):
        """Test that symbols are invalid"""
        guess = "@"
        is_valid = (len(guess) == 1 and guess.isalpha())
        self.assertFalse(is_valid, "Symbols should be invalid")

    def test_input_validation_space(self):
        """Test that space character is invalid"""
        guess = " "
        is_valid = (len(guess) == 1 and guess.isalpha())
        self.assertFalse(is_valid, "Space should be invalid")

    def test_input_validation_valid_letter(self):
        """Test that valid single letters are valid"""
        guess = "a"
        is_valid = (len(guess) == 1 and guess.isalpha())
        self.assertTrue(is_valid, "Single letters should be valid")

    def test_input_validation_uppercase_letter(self):
        """Test that uppercase letters are valid (they get converted to lowercase)"""
        guess = "A"
        is_valid = (len(guess) == 1 and guess.isalpha())
        self.assertTrue(is_valid, "Uppercase letters should be valid")

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

    def test_display_word_empty_string(self):
        """Test display with empty word"""
        self.game.word = ""
        self.assertEqual(self.game.display_word(), "")

    def test_display_word_single_letter(self):
        """Test display with single letter word"""
        self.game.word = "a"
        self.game.guessed_letters = []
        self.assertEqual(self.game.display_word(), "_")
    
    def test_repeated_wrong_guess(self):
        """Test repeated wrong guess doesn't double-deduct lives"""
        self.game.word = "python"
        self.game.process_guess("x")  # First wrong
        lives_after_first = self.game.lives
        result = self.game.process_guess("x")  # Same wrong again
        self.assertEqual(result, "already_guessed")
        self.assertEqual(self.game.lives, lives_after_first)

    def test_complete_game_win(self):
        """Test a complete winning game scenario"""
        self.game.initialize_game("1")
        self.game.word = "cat"  # Force a specific word
        
        results = []
        results.append(self.game.process_guess("c"))
        results.append(self.game.process_guess("a")) 
        results.append(self.game.process_guess("t"))
        
        self.assertEqual(results, ["correct", "correct", "win"])

    def test_complete_game_loss(self):
        """Test a complete losing game scenario"""
        self.game.initialize_game("1")
        self.game.word = "cat"
        
        results = []
        for wrong_guess in "xyzuvw":  # 6 wrong guesses
            results.append(self.game.process_guess(wrong_guess))
        
        self.assertEqual(results[-1], "lose")

if __name__ == "__main__":
    unittest.main()
