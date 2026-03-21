"""Tests for the scikit-learn feature extraction engine."""

import unittest
from sparse import parse


class TestSklearnEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import sklearn  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("scikit-learn not installed")

    def test_sklearn_tokenize(self):
        tokens = parse("Hello world", engine="sklearn", tokenize=True)
        self.assertIsInstance(tokens, list)
        self.assertIn("Hello", tokens)

    def test_sklearn_count_vector(self):
        vec = parse("Hello world", engine="sklearn", tokenize=False, vectorizer="count")
        self.assertFalse(vec.shape[0] == 0)

    def test_sklearn_tfidf_vector(self):
        vec = parse("Hello world", engine="sklearn", tokenize=False, vectorizer="tfidf")
        self.assertFalse(vec.shape[0] == 0)


if __name__ == '__main__':
    unittest.main()
