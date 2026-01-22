import unittest
from sparse import parse
from sparse import utils


class TestSparseUtils(unittest.TestCase):
    """Test the lightweight utility functions."""
    
    def test_lowercase(self):
        """Test lowercase utility."""
        assert utils.lowercase("HELLO WORLD") == "hello world"
        assert utils.lowercase("HeLLo") == "hello"
        assert utils.lowercase("already_lowercase") == "already_lowercase"
    
    def test_remove_punctuation(self):
        """Test punctuation removal."""
        assert utils.remove_punctuation("Hello, World!") == "Hello World"
        assert utils.remove_punctuation("test-case") == "testcase"
        assert utils.remove_punctuation("no punctuation") == "no punctuation"


class TestSparse(unittest.TestCase):
    """Test the main parse function."""
    
    def test_parse_basic(self):
        """Test parse returns input unchanged by default."""
        result = parse("Hello World!")
        self.assertEqual(result, "Hello World!")
    
    def test_parse_lowercase(self):
        """Test parse with lowercase option."""
        result = parse("HELLO WORLD", lowercase=True)
        self.assertEqual(result, "hello world")
    
    def test_parse_remove_punctuation(self):
        """Test parse with remove_punctuation option."""
        result = parse("Hello, World!", remove_punctuation=True)
        self.assertEqual(result, "Hello World")
    
    def test_parse_combined_options(self):
        """Test parse with multiple options."""
        result = parse("HELLO, WORLD!", lowercase=True, remove_punctuation=True)
        self.assertEqual(result, "hello world")
    
    def test_parse_unknown_engine_raises_error(self):
        """Test that unknown engine raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            parse("test", engine="unknown_engine")
        self.assertIn("Unknown engine", str(ctx.exception))
    
    def test_parse_nltk_engine_not_installed_raises_error(self):
        """Test that NLTK engine raises error if nltk not installed."""
        # This test will pass if nltk is not installed, 
        # or fail if nltk is installed (expected behavior).
        try:
            result = parse("test", engine="nltk")
            # If we reach here, nltk is installed; test passes.
            self.assertIsNotNone(result)
        except ValueError as e:
            # If nltk not installed, we expect this error
            self.assertIn("NLTK", str(e))


class TestNLTKEngine(unittest.TestCase):
    """Test suite for NLTK engine (stub for future implementation)."""
    
    def test_nltk_tokenize(self):
        """Test NLTK tokenization (when implemented)."""
        # TODO: Implement when NLTK engine is built
        # result = parse("Hello world", engine="nltk", tokenize=True)
        # self.assertIsInstance(result, list)
        pass
    
    def test_nltk_remove_stopwords(self):
        """Test NLTK stop word removal (when implemented)."""
        # TODO: Implement when NLTK engine is built
        # result = parse("The quick brown fox", engine="nltk", remove_stopwords=True)
        # self.assertNotIn("the", result.lower())
        pass
    
    def test_nltk_lemmatize(self):
        """Test NLTK lemmatization (when implemented)."""
        # TODO: Implement when NLTK engine is built
        # result = parse("running", engine="nltk", lemmatize=True, tokenize=True)
        # self.assertIn("run", result)
        pass


if __name__ == '__main__':
    unittest.main()