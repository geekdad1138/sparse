"""Tests for the SentencePiece engine."""

import unittest
from sparse import parse


class TestSentencePieceEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import sentencepiece  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("SentencePiece not installed")

    def test_sentencepiece_tokenize(self):
        # This test assumes a model file exists; in practice, skip if not
        try:
            result = parse("Hello world", engine="sentencepiece", tokenize=True, model_file="dummy.model")
        except RuntimeError:
            raise unittest.SkipTest("SentencePiece model not available")
        self.assertIsInstance(result, list)

    def test_sentencepiece_joined(self):
        try:
            joined = parse("Hello world", engine="sentencepiece", tokenize=False, model_file="dummy.model")
        except RuntimeError:
            raise unittest.SkipTest("SentencePiece model not available")
        self.assertIsInstance(joined, str)


if __name__ == '__main__':
    unittest.main()
