"""Tests for TextBlob engine."""

import unittest
from sparse import parse


class TestTextBlobEngine(unittest.TestCase):
    """Test suite for TextBlob engine."""
    
    @classmethod
    def setUpClass(cls):
        """Skip tests if TextBlob is not installed."""
        try:
            import textblob
        except ImportError:
            raise unittest.SkipTest("TextBlob not installed")
    
    def test_textblob_tokenize(self):
        """Test TextBlob tokenization."""
        result = parse("Hello world", engine="textblob", tokenize=True)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIn("Hello", result)
        self.assertIn("world", result)
    
    def test_textblob_remove_stopwords(self):
        """Test TextBlob stop word removal."""
        result = parse("The quick brown fox", engine="textblob",
                      remove_stopwords=True, tokenize=True)
        self.assertIsInstance(result, list)
        # "the" should be removed (stop word)
        self.assertNotIn("The", result)
        self.assertNotIn("the", result)
        # Content words should remain
        self.assertIn("quick", result)
        self.assertIn("brown", result)
    
    def test_textblob_lemmatize(self):
        """Test TextBlob lemmatization."""
        result = parse("cats dogs running", engine="textblob",
                      lemmatize=True, tokenize=True)
        self.assertIsInstance(result, list)
        # Check lemmatized forms
        self.assertIn("cat", result)
        self.assertIn("dog", result)
    
    def test_textblob_remove_punctuation(self):
        """Test TextBlob punctuation removal."""
        result = parse("Hello, world!", engine="textblob",
                      remove_punctuation=True, tokenize=True)
        self.assertIsInstance(result, list)
        # Punctuation should be removed
        self.assertNotIn(",", result)
        self.assertNotIn("!", result)
        self.assertIn("Hello", result)
        self.assertIn("world", result)
    
    def test_textblob_lowercase(self):
        """Test TextBlob lowercase conversion."""
        result = parse("HELLO WORLD", engine="textblob",
                      lowercase=True, tokenize=True)
        self.assertIsInstance(result, list)
        self.assertIn("hello", result)
        self.assertIn("world", result)
    
    def test_textblob_combined_options(self):
        """Test TextBlob with multiple options."""
        result = parse("The QUICK BROWN FOX", engine="textblob",
                      lowercase=True, remove_stopwords=True, tokenize=True)
        self.assertIsInstance(result, list)
        # "the" is a stop word, should be removed
        self.assertNotIn("the", result)
        # Other words should be lowercase
        self.assertIn("quick", result)
        self.assertIn("brown", result)
    
    def test_textblob_joined_output(self):
        """Test TextBlob with joined string output."""
        result = parse("Hello world", engine="textblob", tokenize=False)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Hello world")
    
    def test_textblob_sentiment(self):
        """Test TextBlob sentiment analysis."""
        # Positive sentiment
        positive = parse("I love this!", engine="textblob", sentiment=True)
        self.assertIsInstance(positive, dict)
        self.assertIn("polarity", positive)
        self.assertIn("subjectivity", positive)
        self.assertGreater(positive["polarity"], 0.5)  # Should be positive
        
        # Negative sentiment
        negative = parse("I hate this", engine="textblob", sentiment=True)
        self.assertIsInstance(negative, dict)
        self.assertLess(negative["polarity"], -0.3)  # Should be negative
        
        # Neutral sentiment
        neutral = parse("The cat is on the mat", engine="textblob", sentiment=True)
        self.assertIsInstance(neutral, dict)
        # Neutral should have low polarity magnitude
        self.assertLess(abs(neutral["polarity"]), 0.3)
    
    def test_textblob_noun_phrases(self):
        """Test TextBlob noun phrase extraction."""
        result = parse("The quick brown fox jumps over the lazy dog",
                      engine="textblob", noun_phrases=True)
        self.assertIsInstance(result, list)
        # Should extract noun phrases
        self.assertGreater(len(result), 0)
        # Check for expected phrases (exact matching depends on TextBlob)
        phrase_text = ' '.join(result).lower()
        self.assertIn("fox", phrase_text)
    
    def test_textblob_sentiment_subjectivity(self):
        """Test TextBlob sentiment subjectivity dimension."""
        # Subjective (opinion-based)
        subjective = parse("I think this is amazing!", engine="textblob", sentiment=True)
        self.assertGreater(subjective["subjectivity"], 0.5)
        
        # Objective (fact-based)
        objective = parse("Water boils at 100 degrees Celsius", engine="textblob", sentiment=True)
        self.assertLess(objective["subjectivity"], 0.5)


if __name__ == '__main__':
    unittest.main()
