"""Tests for the Gensim engine."""

import unittest
from sparse import parse


class TestGensimEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import gensim  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("Gensim not installed")

    def test_gensim_tokenize(self):
        result = parse("Hello world", engine="gensim", tokenize=True)
        self.assertIsInstance(result, list)
        self.assertEqual(result, ["hello", "world"])

    def test_gensim_remove_stopwords(self):
        result = parse("The quick brown fox", engine="gensim", tokenize=True, remove_stopwords=True)
        self.assertNotIn("the", result)
        self.assertIn("quick", result)

    def test_gensim_lemmatize(self):
        # Only run this test if NLTK is installed (required for lemmatization)
        try:
            import nltk  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("NLTK not installed")

        result = parse("cats dogs running", engine="gensim", tokenize=True, lemmatize=True)
        self.assertIn("cat", result)
        self.assertIn("dog", result)

    def test_gensim_joined(self):
        joined = parse("Hello world", engine="gensim", tokenize=False)
        self.assertIsInstance(joined, str)
        self.assertEqual(joined, "hello world")


if __name__ == '__main__':
    unittest.main()
