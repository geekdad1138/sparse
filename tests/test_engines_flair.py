"""Tests for the Flair engine."""

import unittest
from sparse import parse


class TestFlairEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import flair  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("Flair not installed")

    def test_flair_tokenize(self):
        result = parse("Hello world", engine="flair", tokenize=True)
        self.assertIsInstance(result, list)
        self.assertIn("Hello", result)

    def test_flair_joined(self):
        joined = parse("Hello world", engine="flair", tokenize=False)
        self.assertIsInstance(joined, str)

    def test_flair_ner(self):
        # NER might require model download; skip if fails
        try:
            ents = parse("Apple is in Cupertino", engine="flair", ner=True)
            self.assertIsInstance(ents, list)
        except RuntimeError:
            raise unittest.SkipTest("Flair NER model not available")

    def test_flair_pos_tag(self):
        try:
            tagged = parse("Hello world", engine="flair", pos_tag=True)
            self.assertIsInstance(tagged, list)
            if tagged:
                self.assertIsInstance(tagged[0], tuple)
        except RuntimeError:
            raise unittest.SkipTest("Flair POS model not available")


if __name__ == '__main__':
    unittest.main()
