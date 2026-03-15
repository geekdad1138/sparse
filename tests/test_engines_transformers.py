"""Tests for the Transformers engine."""

import unittest
from sparse import parse


class TestTransformersEngine(unittest.TestCase):
    """Basic sanity checks for the transformers engine."""

    @classmethod
    def setUpClass(cls):
        try:
            import transformers  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("Transformers not installed")

    def test_transformers_tokenize(self):
        result = parse("Hello world", engine="transformers", tokenize=True)
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 1)
        # bert-base-uncased lowercases input
        self.assertEqual(result[0], "hello")

    def test_transformers_return_ids(self):
        tokens = parse("Hello world", engine="transformers", tokenize=True)
        ids = parse("Hello world", engine="transformers", tokenize=True, return_ids=True)
        self.assertIsInstance(ids, list)
        self.assertEqual(len(ids), len(tokens))
        self.assertTrue(all(isinstance(i, int) for i in ids))

    def test_transformers_joined(self):
        joined = parse("Hello world", engine="transformers", tokenize=False)
        self.assertIsInstance(joined, str)
        self.assertEqual(joined, "hello world")

    def test_unknown_model_raises(self):
        with self.assertRaises(RuntimeError):
            parse("test", engine="transformers", model_name="nonexistent-model")


if __name__ == '__main__':
    unittest.main()
