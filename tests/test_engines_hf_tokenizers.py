"""Tests for the Hugging Face Tokenizers engine."""

import unittest
from sparse import parse


class TestHFTokenizersEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import tokenizers  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("Tokenizers not installed")

    def test_hf_tokenizers_tokenize(self):
        result = parse("Hello world", engine="hf_tokenizers", tokenize=True)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_hf_tokenizers_return_ids(self):
        ids = parse("Hello world", engine="hf_tokenizers", tokenize=True, return_ids=True)
        self.assertIsInstance(ids, list)
        self.assertTrue(all(isinstance(i, int) for i in ids))

    def test_hf_tokenizers_joined(self):
        joined = parse("Hello world", engine="hf_tokenizers", tokenize=False)
        self.assertIsInstance(joined, str)


if __name__ == '__main__':
    unittest.main()
