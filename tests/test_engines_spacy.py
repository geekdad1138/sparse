"""Tests for spaCy engine."""

import unittest
from sparse import parse


class TestSpaCyEngine(unittest.TestCase):
    """Test suite for spaCy engine."""
    
    @classmethod
    def setUpClass(cls):
        """Skip tests if spacy is not installed."""
        try:
            import spacy
            try:
                spacy.load('en_core_web_sm')
            except OSError:
                raise unittest.SkipTest("spaCy model 'en_core_web_sm' not installed")
        except ImportError:
            raise unittest.SkipTest("spaCy not installed")
    
    def test_spacy_tokenize(self):
        """Test spaCy tokenization."""
        result = parse("Hello world", engine="spacy", tokenize=True)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIn("Hello", result)
        self.assertIn("world", result)
    
    def test_spacy_remove_stopwords(self):
        """Test spaCy stop word removal."""
        result = parse("The quick brown fox", engine="spacy", 
                      remove_stopwords=True, tokenize=True)
        self.assertIsInstance(result, list)
        # "the" should be removed (stop word)
        self.assertNotIn("The", result)
        self.assertNotIn("the", result)
        # Content words should remain
        self.assertIn("quick", result)
        self.assertIn("brown", result)
    
    def test_spacy_lemmatize(self):
        """Test spaCy lemmatization."""
        result = parse("cats dogs running", engine="spacy", 
                      lemmatize=True, tokenize=True)
        self.assertIsInstance(result, list)
        # Check lemmatized forms
        self.assertIn("cat", result)
        self.assertIn("dog", result)
    
    def test_spacy_remove_punctuation(self):
        """Test spaCy punctuation removal."""
        result = parse("Hello, world!", engine="spacy", 
                      remove_punctuation=True, tokenize=True)
        self.assertIsInstance(result, list)
        # No punctuation tokens should remain
        self.assertNotIn(",", result)
        self.assertNotIn("!", result)
        self.assertIn("Hello", result)
        self.assertIn("world", result)
    
    def test_spacy_lowercase(self):
        """Test spaCy lowercase conversion."""
        result = parse("HELLO WORLD", engine="spacy", 
                      lowercase=True, tokenize=True)
        self.assertIsInstance(result, list)
        self.assertIn("hello", result)
        self.assertIn("world", result)
    
    def test_spacy_combined_options(self):
        """Test spaCy with multiple options."""
        result = parse("THE QUICK BROWN FOX", engine="spacy",
                      lowercase=True, remove_stopwords=True, 
                      tokenize=True)
        self.assertIsInstance(result, list)
        # "the" is a stop word, should be removed
        self.assertNotIn("the", result)
        # Other words should be lowercase
        self.assertIn("quick", result)
        self.assertIn("brown", result)
    
    def test_spacy_joined_output(self):
        """Test spaCy with joined string output (no tokenize)."""
        result = parse("Hello world", engine="spacy", tokenize=False)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Hello world")
    
    def test_spacy_pos_tag(self):
        """Test spaCy POS tagging."""
        result = parse("Hello world", engine="spacy", 
                      pos_tag=True, tokenize=True)
        self.assertIsInstance(result, list)
        # Results should be tuples of (token, pos)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], tuple)
        self.assertEqual(len(result[0]), 2)
        # Check token text and POS tag exist
        token_text, pos = result[0]
        self.assertEqual(token_text, "Hello")
        self.assertIsNotNone(pos)
    
    def test_spacy_ner(self):
        """Test spaCy Named Entity Recognition."""
        result = parse("Apple is in Cupertino", engine="spacy", ner=True)
        self.assertIsInstance(result, list)
        # Should have entities
        self.assertGreater(len(result), 0)
        # Check entity structure
        entity = result[0]
        self.assertIn("text", entity)
        self.assertIn("label", entity)
        self.assertIn("start", entity)
        self.assertIn("end", entity)


if __name__ == '__main__':
    unittest.main()
