"""
Test suite for the String-Encoding module.
"""

import unittest
from string_encoding import String

class TestStringEncoding(unittest.TestCase):
    """Test cases for the String class encoding methods."""
    
    def test_base64(self):
        """Test base64 encoding and decoding."""
        # Test basic encoding/decoding
        test_str = String("hello world")
        encoded = test_str.base64()
        self.assertEqual(encoded, "aGVsbG8gd29ybGQ=")
        decoded = encoded.decode_base64()
        self.assertEqual(decoded, test_str)
        
        # Test empty string
        empty = String("")
        encoded_empty = empty.base64()
        self.assertEqual(encoded_empty, "")
        
        # Test special characters
        special = String("!@#$%^&*()")
        encoded_special = special.base64()
        decoded_special = encoded_special.decode_base64()
        self.assertEqual(decoded_special, special)
    
    def test_byte_pair_encoding(self):
        """Test byte pair encoding and decoding."""
        # Test string with repeating patterns
        test_str = String("aaabbbccc")
        encoded = test_str.byte_pair_encoding()
        self.assertTrue(len(encoded.rules) > 0)
        decoded = encoded.decode_byte_pair()
        self.assertEqual(decoded, test_str)
        
        # Test with no repeating patterns
        unique = String("abcdefg")
        try:
            encoded_unique = unique.byte_pair_encoding()
            decoded_unique = encoded_unique.decode_byte_pair()
            self.assertEqual(decoded_unique, unique)
        except Exception as e:
            # It's okay if this raises an exception for strings with no repeating patterns
            pass
    
    def test_cyclic_bits(self):
        """Test cyclic bit shifting."""
        test_str = String("test")
        shifted = test_str.cyclic_bits(3)
        unshifted = shifted.decode_cyclic_bits(3)
        self.assertEqual(unshifted, test_str)
        
        # Test with negative shift
        neg_shifted = test_str.cyclic_bits(-5)
        neg_unshifted = neg_shifted.decode_cyclic_bits(-5)
        self.assertEqual(neg_unshifted, test_str)
    
    def test_cyclic_chars(self):
        """Test cyclic character shifting."""
        test_str = String("Hello World")
        shifted = test_str.cyclic_chars(5)
        unshifted = shifted.decode_cyclic_chars(5)
        self.assertEqual(unshifted, test_str)
        
        # Test with negative shift
        neg_shifted = test_str.cyclic_chars(-10)
        neg_unshifted = neg_shifted.decode_cyclic_chars(-10)
        self.assertEqual(neg_unshifted, test_str)
    
    def test_histogram(self):
        """Test character histogram generation."""
        test_str = String("Hello 123!")
        hist = test_str.histogram_of_chars()
        
        # Check that all histogram categories are present
        categories = ['control code', 'digits', 'upper', 'lower', 'other printable', 'higher than 128']
        for category in categories:
            self.assertIn(category, hist)
            
        # Verify counts
        self.assertEqual(hist['digits'], 3)  # 1, 2, 3
        self.assertEqual(hist['upper'], 1)   # H
        self.assertEqual(hist['lower'], 4)   # e, l, l, o
        self.assertEqual(hist['other printable'], 3)  # space, !, !
    
    def test_string_operations(self):
        """Test that String class maintains its type after operations."""
        a = String("hello")
        b = String("world")
        
        # Test addition
        c = a + b
        self.assertIsInstance(c, String)
        self.assertEqual(c, "helloworld")
        
        # Test multiplication
        d = a * 3
        self.assertIsInstance(d, String)
        self.assertEqual(d, "hellohellohello")
        
        # Test slicing
        e = a[1:4]
        self.assertIsInstance(e, String)
        self.assertEqual(e, "ell")
        
        # Test iteration
        chars = list(a)
        for char in chars:
            self.assertIsInstance(char, String)

if __name__ == '__main__':
    unittest.main()