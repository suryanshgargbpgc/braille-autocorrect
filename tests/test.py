import unittest
import sys
import os
import tempfile

# Add parent directory to path to import project modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autocorrect import AutoCorrect
from utils import levenshtein_distance

class TestLevenshteinDistance(unittest.TestCase):
    
    def test_identical_strings(self):
        """Test distance between identical strings"""
        self.assertEqual(levenshtein_distance('cat', 'cat'), 0)
        self.assertEqual(levenshtein_distance('hello', 'hello'), 0)
    
    def test_single_character_operations(self):
        """Test single character insertions, deletions, substitutions"""
        # Single insertion
        self.assertEqual(levenshtein_distance('cat', 'cats'), 1)
        
        # Single deletion
        self.assertEqual(levenshtein_distance('cats', 'cat'), 1)
        
        # Single substitution
        self.assertEqual(levenshtein_distance('cat', 'car'), 1)
    
    def test_multiple_operations(self):
        """Test multiple character operations"""
        self.assertEqual(levenshtein_distance('kitten', 'sitting'), 3)
        self.assertEqual(levenshtein_distance('saturday', 'sunday'), 3)
    
    def test_empty_strings(self):
        """Test with empty strings"""
        self.assertEqual(levenshtein_distance('', 'abc'), 3)
        self.assertEqual(levenshtein_distance('abc', ''), 3)
        self.assertEqual(levenshtein_distance('', ''), 0)


class TestAutoCorrect(unittest.TestCase):
    
    def setUp(self):
        """Set up test dictionary"""
        # Create a temporary dictionary file
        self.temp_dict = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        test_words = ['cat', 'car', 'card', 'dog', 'door', 'hello', 'world', 'test', 'braille']
        for word in test_words:
            self.temp_dict.write(word + '\n')
        self.temp_dict.close()
        
        self.autocorrect = AutoCorrect(self.temp_dict.name)
    
    def tearDown(self):
        """Clean up temporary files"""
        os.unlink(self.temp_dict.name)
    
    def test_exact_match(self):
        """Test suggestions for exact matches"""
        suggestions = self.autocorrect.suggest('cat')
        self.assertIn('cat', suggestions)
        self.assertEqual(suggestions[0], 'cat')  # Exact match should be first
    
    def test_single_character_typo(self):
        """Test suggestions for single character typos"""
        suggestions = self.autocorrect.suggest('cay')  # 'cat' with 'y' instead of 't'
        self.assertIn('cat', suggestions)
        
        suggestions = self.autocorrect.suggest('dar')  # 'car' with 'd' instead of 'c'
        self.assertIn('car', suggestions)
    
    def test_missing_character(self):
        """Test suggestions for missing characters"""
        suggestions = self.autocorrect.suggest('ca')  # Missing 't' from 'cat'
        self.assertIn('cat', suggestions)
        self.assertIn('car', suggestions)
    
    def test_extra_character(self):
        """Test suggestions for extra characters"""
        suggestions = self.autocorrect.suggest('cats')  # Extra 's' in 'cat'
        self.assertIn('cat', suggestions)
    
    def test_max_cost_limit(self):
        """Test max_cost parameter limits results"""
        # Test with very strict cost
        suggestions = self.autocorrect.suggest('xyz', max_cost=1)
        self.assertEqual(len(suggestions), 0)  # No words within cost 1
        
        # Test with looser cost
        suggestions = self.autocorrect.suggest('xyz', max_cost=3)
        self.assertTrue(len(suggestions) > 0)  # Should find some words
    
    def test_result_limit(self):
        """Test limit parameter controls number of results"""
        suggestions = self.autocorrect.suggest('c', limit=2)
        self.assertLessEqual(len(suggestions), 2)
        
        suggestions = self.autocorrect.suggest('c', limit=5)
        self.assertLessEqual(len(suggestions), 5)
    
    def test_empty_input(self):
        """Test behavior with empty input"""
        suggestions = self.autocorrect.suggest('')
        self.assertIsInstance(suggestions, list)
    
    def test_nonexistent_word(self):
        """Test suggestions for completely made-up words"""
        suggestions = self.autocorrect.suggest('qwerty')
        # Should return some suggestions based on edit distance
        self.assertIsInstance(suggestions, list)
    
    def test_case_sensitivity(self):
        """Test that suggestions work regardless of input case"""
        suggestions_lower = self.autocorrect.suggest('cat')
        suggestions_upper = self.autocorrect.suggest('CAT')
        suggestions_mixed = self.autocorrect.suggest('CaT')
        
        # All should find 'cat' since dictionary is lowercase
        self.assertIn('cat', suggestions_lower)
        self.assertIn('cat', suggestions_upper)
        self.assertIn('cat', suggestions_mixed)


class TestAutoCorrectIntegration(unittest.TestCase):
    
    def setUp(self):
        """Set up with default dictionary"""
        # Use the actual dictionary.txt file if it exists
        dict_path = 'dictionary.txt'
        if not os.path.exists(dict_path):
            # Create minimal dictionary for testing
            self.temp_dict = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
            self.temp_dict.write('cat\ncar\ndog\nhello\nworld\n')
            self.temp_dict.close()
            dict_path = self.temp_dict.name
        else:
            self.temp_dict = None
        
        self.autocorrect = AutoCorrect(dict_path)
    
    def tearDown(self):
        """Clean up if temporary file was created"""
        if self.temp_dict:
            os.unlink(self.temp_dict.name)
    
    def test_braille_word_correction(self):
        """Test autocorrect with typical Braille decoding errors"""
        # Common Braille transcription errors
        suggestions = self.autocorrect.suggest('ca')  # Missing last character
        self.assertTrue(len(suggestions) > 0)
        
        suggestions = self.autocorrect.suggest('caat')  # Extra character
        self.assertTrue(len(suggestions) > 0)


if __name__ == '__main__':
    unittest.main()
